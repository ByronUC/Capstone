from typing import Any
import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select
from pydantic import BaseModel, EmailStr

from app import crud
from app.api.deps import SessionDep
from app.models import (
    Message,
    Cita,
    CitaCreate,
    CitaPublic,
    CitasPublic,
    CitaUpdate,
    Paciente,
    PacienteCreate,
    SalaAtencion,
    Notificacion,
)
from app.services.email_service import EmailService
from app.services.calendar_service import calendar_service

router = APIRouter(prefix="/citas", tags=["citas"])


# Schemas adicionales para el sistema de reservas
class ReservaCreate(BaseModel):
    """Schema para crear una reserva desde el formulario web"""
    # Datos del paciente
    rut: str
    nombres: str
    apellido_paterno: str
    apellido_materno: str | None = None
    telefono: str
    email: EmailStr
    fecha_nacimiento: str  # YYYY-MM-DD

    # Datos de la cita
    id_servicio: int
    id_psicologo: int
    fecha_cita: str  # YYYY-MM-DD
    hora_inicio: str  # HH:MM
    hora_fin: str  # HH:MM
    motivo_consulta: str | None = None


class ReagendarRequest(BaseModel):
    """Schema para reagendar una cita"""
    nueva_fecha: str  # YYYY-MM-DD
    nueva_hora_inicio: str  # HH:MM
    nueva_hora_fin: str  # HH:MM


@router.get("/", response_model=CitasPublic)
def read_citas(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Obtener lista de citas.

    Retorna citas programadas con filtros por fecha, estado (pendiente/confirmada/
    completada/cancelada), cliente o empleado asignado. Incluye paginación y
    ordenamiento por fecha.
    """
    count_statement = select(func.count()).select_from(Cita)
    count = session.exec(count_statement).one()

    statement = select(Cita).offset(skip).limit(limit)
    citas = session.exec(statement).all()

    return CitasPublic(data=citas, count=count)


@router.get("/{codigo_confirmacion}", response_model=CitaPublic)
def get_cita_by_codigo(codigo_confirmacion: str, session: SessionDep) -> Any:
    """
    GET /api/citas/{codigo_confirmacion}

    Busca y retorna información de una cita por su código de confirmación.

    Respuesta: datos completos de la cita incluyendo paciente, psicólogo,
    servicio, fecha, hora, estado.
    """
    statement = select(Cita).where(Cita.codigo_confirmacion == codigo_confirmacion)
    cita = session.exec(statement).first()

    if not cita:
        raise HTTPException(
            status_code=404,
            detail="No se encontró una cita con ese código de confirmación",
        )

    return cita


@router.post("/", response_model=dict)
def create_reserva(*, session: SessionDep, reserva: ReservaCreate) -> Any:
    """
    POST /api/citas

    Crea una nueva cita desde el formulario web de pacientes.

    Lógica:
    1. Validar que el horario siga disponible (double-check)
    2. Insertar/actualizar paciente en tabla pacientes
    3. Insertar cita en tabla citas con estado "Pendiente"
    4. Generar código único de confirmación (UUID)
    5. Asignar sala automáticamente
    6. Crear registro en tabla notificaciones para enviar email

    Respuesta: código de confirmación
    """
    # 1. Validar disponibilidad del horario (evitar doble reserva)
    from datetime import date, time
    fecha_cita = date.fromisoformat(reserva.fecha_cita)
    hora_inicio = time.fromisoformat(reserva.hora_inicio)
    hora_fin = time.fromisoformat(reserva.hora_fin)

    # Verificar si ya existe una cita en ese horario
    statement = select(Cita).where(
        Cita.id_psicologo == reserva.id_psicologo,
        Cita.fecha_cita == fecha_cita,
        Cita.hora_inicio == hora_inicio,
        Cita.id_estado_cita.in_([1, 2])  # Pendiente o Confirmada
    )
    cita_existente = session.exec(statement).first()

    if cita_existente:
        raise HTTPException(
            status_code=409,
            detail="El horario seleccionado ya no está disponible. Por favor seleccione otro horario."
        )

    # 2. Insertar/actualizar paciente
    paciente_existente = crud.get_paciente_by_rut(session=session, rut=reserva.rut)

    if paciente_existente:
        # Actualizar datos del paciente existente
        paciente_existente.nombres = reserva.nombres
        paciente_existente.apellido_paterno = reserva.apellido_paterno
        paciente_existente.apellido_materno = reserva.apellido_materno
        paciente_existente.telefono = reserva.telefono
        paciente_existente.email = reserva.email
        session.add(paciente_existente)
        session.commit()
        session.refresh(paciente_existente)
        paciente = paciente_existente
    else:
        # Crear nuevo paciente
        paciente_data = PacienteCreate(
            rut=reserva.rut,
            nombres=reserva.nombres,
            apellido_paterno=reserva.apellido_paterno,
            apellido_materno=reserva.apellido_materno,
            fecha_nacimiento=date.fromisoformat(reserva.fecha_nacimiento),
            telefono=reserva.telefono,
            email=reserva.email,
        )
        paciente = crud.create_paciente(session=session, paciente_create=paciente_data)

    # 3. Generar código único de confirmación
    codigo_confirmacion = str(uuid.uuid4())[:8].upper()  # Primeros 8 caracteres del UUID

    # 4. Buscar estado "Pendiente" (asumimos que es id_estado_cita = 1)
    id_estado_pendiente = 1  # TODO: Buscar dinámicamente desde la BD

    # 5. Asignar sala automáticamente
    statement = select(SalaAtencion).where(SalaAtencion.estado == 'disponible')
    sala = session.exec(statement).first()
    id_sala = sala.id_sala if sala else None

    # 6. Crear la cita con estado "Pendiente"
    cita_data = CitaCreate(
        id_paciente=paciente.id_paciente,
        id_psicologo=reserva.id_psicologo,
        id_servicio=reserva.id_servicio,
        id_sala=id_sala,
        id_estado_cita=id_estado_pendiente,
        fecha_cita=fecha_cita,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin,
        motivo_consulta=reserva.motivo_consulta,
    )

    cita = crud.create_cita(session=session, cita_create=cita_data)

    # Actualizar el código de confirmación
    cita.codigo_confirmacion = codigo_confirmacion
    session.add(cita)
    session.commit()
    session.refresh(cita)

    # 7. Crear notificación de email para el paciente
    # Cargar relaciones necesarias
    session.refresh(cita, ["paciente", "psicologo", "servicio"])

    nombre_completo = f"{paciente.nombres} {paciente.apellido_paterno}"
    nombre_psicologo = f"{cita.psicologo.nombres} {cita.psicologo.apellido_paterno}"
    nombre_servicio = cita.servicio.nombre_servicio

    # Crear y enviar notificaciones (paciente + psicólogo)
    EmailService.crear_notificacion_confirmacion_inicial(
        session=session,
        cita=cita,
        nombre_paciente=nombre_completo,
        nombre_psicologo=nombre_psicologo,
        nombre_servicio=nombre_servicio
    )

    # Respuesta con el código de confirmación
    return {
        "message": "Cita creada exitosamente",
        "codigo_confirmacion": codigo_confirmacion,
        "id_cita": cita.id_cita,
        "fecha_cita": str(fecha_cita),
        "hora_inicio": str(hora_inicio)
    }


@router.put("/{codigo_confirmacion}/reagendar", response_model=dict)
def reagendar_cita(
    *,
    session: SessionDep,
    codigo_confirmacion: str,
    reagendar: ReagendarRequest
) -> Any:
    """
    PUT /api/citas/{codigo_confirmacion}/reagendar

    Reagenda una cita existente.

    Lógica:
    1. Buscar cita por código
    2. Validar nueva disponibilidad
    3. Actualizar fecha y hora de la cita
    4. Cambiar estado a "Reprogramada"
    5. Crear notificación de reagendamiento
    6. Si existe google_calendar_event_id, actualizar evento en Google Calendar

    Respuesta: confirmación con nuevos datos
    """
    from datetime import date, time

    # 1. Buscar cita por código
    statement = select(Cita).where(Cita.codigo_confirmacion == codigo_confirmacion)
    cita = session.exec(statement).first()

    if not cita:
        raise HTTPException(
            status_code=404,
            detail="No se encontró una cita con ese código de confirmación"
        )

    # Verificar que la cita no esté cancelada
    if cita.id_estado_cita == 5:  # Asumimos que 5 es Cancelada
        raise HTTPException(
            status_code=400,
            detail="No se puede reagendar una cita cancelada"
        )

    # 2. Validar nueva disponibilidad
    nueva_fecha = date.fromisoformat(reagendar.nueva_fecha)
    nueva_hora_inicio = time.fromisoformat(reagendar.nueva_hora_inicio)
    nueva_hora_fin = time.fromisoformat(reagendar.nueva_hora_fin)

    # Verificar si el nuevo horario está disponible
    statement = select(Cita).where(
        Cita.id_psicologo == cita.id_psicologo,
        Cita.fecha_cita == nueva_fecha,
        Cita.hora_inicio == nueva_hora_inicio,
        Cita.id_estado_cita.in_([1, 2]),  # Pendiente o Confirmada
        Cita.id_cita != cita.id_cita  # Excluir la cita actual
    )
    cita_conflicto = session.exec(statement).first()

    if cita_conflicto:
        raise HTTPException(
            status_code=409,
            detail="El nuevo horario ya no está disponible"
        )

    # Guardar fecha/hora antigua para el email
    fecha_antigua = cita.fecha_cita
    hora_antigua_inicio = cita.hora_inicio
    hora_antigua_fin = cita.hora_fin

    # 3. Actualizar fecha y hora de la cita
    cita.fecha_cita = nueva_fecha
    cita.hora_inicio = nueva_hora_inicio
    cita.hora_fin = nueva_hora_fin
    cita.fecha_modificacion = datetime.utcnow()

    # 4. Cambiar estado a "Reprogramada" (asumimos id = 4)
    cita.id_estado_cita = 4

    session.add(cita)
    session.commit()
    session.refresh(cita)

    # 5. Crear y enviar notificación de reagendamiento
    session.refresh(cita, ["paciente", "psicologo", "servicio"])

    nombre_completo = f"{cita.paciente.nombres} {cita.paciente.apellido_paterno}"
    nombre_psicologo = f"{cita.psicologo.nombres} {cita.psicologo.apellido_paterno}"
    nombre_servicio = cita.servicio.nombre_servicio

    # Crear y enviar notificaciones de reagendamiento (paciente + psicólogo)
    EmailService.crear_notificacion_reagendamiento(
        session=session,
        cita=cita,
        nombre_paciente=nombre_completo,
        nombre_psicologo=nombre_psicologo,
        nombre_servicio=nombre_servicio,
        fecha_antigua=fecha_antigua,
        hora_antigua_inicio=hora_antigua_inicio,
        hora_antigua_fin=hora_antigua_fin
    )

    # 6. Actualizar evento en Google Calendar si existe
    if cita.google_calendar_event_id:
        from datetime import datetime as dt
        fecha_hora_inicio = dt.combine(nueva_fecha, nueva_hora_inicio)
        duracion = cita.servicio.duracion_minutos

        calendar_service.update_event(
            event_id=cita.google_calendar_event_id,
            titulo=f"Cita - {nombre_completo} - {nombre_servicio}",
            descripcion=f"Paciente: {nombre_completo}\nPsicólogo: {nombre_psicologo}\nMotivo: {cita.motivo_consulta or 'No especificado'}",
            fecha_inicio=fecha_hora_inicio,
            duracion_minutos=duracion,
            email_paciente=cita.paciente.email,
            email_psicologo=cita.psicologo.email_personal if cita.psicologo.email_personal else None
        )

    return {
        "message": "Cita reagendada exitosamente",
        "codigo_confirmacion": codigo_confirmacion,
        "nueva_fecha": str(nueva_fecha),
        "nueva_hora_inicio": str(nueva_hora_inicio)
    }


@router.delete("/{codigo_confirmacion}/cancelar", response_model=Message)
def cancelar_cita(session: SessionDep, codigo_confirmacion: str) -> Message:
    """
    DELETE /api/citas/{codigo_confirmacion}/cancelar

    Cancela una cita.

    Lógica:
    1. Buscar cita por código
    2. Actualizar estado a "Cancelada"
    3. Liberar horario (no aparecerá como ocupado)
    4. Crear notificaciones de cancelación
    5. Si existe google_calendar_event_id, eliminar evento de Google Calendar

    Respuesta: confirmación de cancelación
    """
    # 1. Buscar cita por código
    statement = select(Cita).where(Cita.codigo_confirmacion == codigo_confirmacion)
    cita = session.exec(statement).first()

    if not cita:
        raise HTTPException(
            status_code=404,
            detail="No se encontró una cita con ese código de confirmación"
        )

    # Verificar que la cita no esté ya cancelada
    if cita.id_estado_cita == 5:  # Asumimos que 5 es Cancelada
        raise HTTPException(
            status_code=400,
            detail="La cita ya está cancelada"
        )

    # 2. Actualizar estado a "Cancelada" (asumimos id = 5)
    cita.id_estado_cita = 5
    cita.fecha_modificacion = datetime.utcnow()

    session.add(cita)
    session.commit()
    session.refresh(cita)

    # 3. Crear y enviar notificación de cancelación
    session.refresh(cita, ["paciente", "psicologo", "servicio"])

    nombre_completo = f"{cita.paciente.nombres} {cita.paciente.apellido_paterno}"
    nombre_psicologo = f"{cita.psicologo.nombres} {cita.psicologo.apellido_paterno}"
    nombre_servicio = cita.servicio.nombre if cita.servicio else ""

    # Crear y enviar notificaciones de cancelación (paciente + psicólogo)
    EmailService.crear_notificacion_cancelacion(
        session=session,
        cita=cita,
        nombre_paciente=nombre_completo,
        nombre_psicologo=nombre_psicologo,
        nombre_servicio=nombre_servicio
    )

    # 4. Eliminar evento de Google Calendar si existe
    if cita.google_calendar_event_id:
        calendar_service.delete_event(cita.google_calendar_event_id)

    return Message(message="Cita cancelada exitosamente")


@router.put("/{id}/confirmar", response_model=dict)
def confirmar_cita(session: SessionDep, id: int) -> Any:
    """
    PUT /api/citas/{id}/confirmar

    Endpoint para que recepcionista confirme una cita (desde app escritorio).

    Lógica:
    1. Actualizar estado de "Pendiente" a "Confirmada"
    2. Crear notificaciones para paciente y psicólogo
    3. Crear evento en Google Calendar
    4. Guardar google_calendar_event_id en la cita

    Respuesta: confirmación
    """
    # 1. Buscar cita
    cita = session.get(Cita, id)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    # Verificar que esté en estado "Pendiente"
    if cita.id_estado_cita != 1:
        raise HTTPException(
            status_code=400,
            detail="Solo se pueden confirmar citas en estado Pendiente"
        )

    # 2. Actualizar estado a "Confirmada" (asumimos id = 2)
    cita.id_estado_cita = 2
    cita.fecha_modificacion = datetime.utcnow()

    session.add(cita)
    session.commit()
    session.refresh(cita)

    # 3. Crear y enviar notificación de confirmación final
    session.refresh(cita, ["paciente", "psicologo", "servicio"])

    nombre_completo = f"{cita.paciente.nombres} {cita.paciente.apellido_paterno}"
    nombre_psicologo = f"{cita.psicologo.nombres} {cita.psicologo.apellido_paterno}"
    nombre_servicio = cita.servicio.nombre_servicio

    # Crear y enviar notificaciones de confirmación final (paciente + psicólogo)
    EmailService.crear_notificacion_confirmacion_final(
        session=session,
        cita=cita,
        nombre_paciente=nombre_completo,
        nombre_psicologo=nombre_psicologo,
        nombre_servicio=nombre_servicio
    )

    # 4. Crear evento en Google Calendar y guardar event_id
    from datetime import datetime as dt
    fecha_hora_inicio = dt.combine(cita.fecha_cita, cita.hora_inicio)
    duracion = cita.servicio.duracion_minutos

    event_id = calendar_service.create_event(
        titulo=f"Cita - {nombre_completo} - {nombre_servicio}",
        descripcion=f"Paciente: {nombre_completo}\nPsicólogo: {nombre_psicologo}\nMotivo: {cita.motivo_consulta or 'No especificado'}",
        fecha_inicio=fecha_hora_inicio,
        duracion_minutos=duracion,
        email_paciente=cita.paciente.email,
        email_psicologo=cita.psicologo.email_personal if cita.psicologo.email_personal else None
    )

    if event_id:
        cita.google_calendar_event_id = event_id
        session.add(cita)
        session.commit()

    return {
        "message": "Cita confirmada exitosamente",
        "id_cita": cita.id_cita,
        "estado": "Confirmada"
    }


@router.get("/pendientes/lista", response_model=CitasPublic)
def get_citas_pendientes(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    GET /api/citas/pendientes/lista

    Endpoint para que la aplicación de escritorio obtenga todas las citas pendientes.

    Retorna: Lista de citas con estado "Pendiente" ordenadas por fecha.
    """
    # Buscar todas las citas con estado "Pendiente" (id = 1)
    count_statement = select(func.count()).select_from(Cita).where(Cita.id_estado_cita == 1)
    count = session.exec(count_statement).one()

    statement = (
        select(Cita)
        .where(Cita.id_estado_cita == 1)
        .order_by(Cita.fecha_cita, Cita.hora_inicio)
        .offset(skip)
        .limit(limit)
    )
    citas = session.exec(statement).all()

    return CitasPublic(data=citas, count=count)


@router.put("/{id}/marcar-presente", response_model=dict)
def marcar_paciente_presente(session: SessionDep, id: int) -> Any:
    """
    PUT /api/citas/{id}/marcar-presente

    Endpoint para que recepcionista marque que el paciente llegó a la cita.

    Lógica:
    1. Actualizar estado de "confirmada" a "paciente_presente" (id_estado_cita = 9)
    2. Crear notificación para el psicólogo avisando que el paciente llegó

    Respuesta: confirmación con id_cita y nuevo estado
    """
    # 1. Buscar cita
    cita = session.get(Cita, id)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    # Verificar que esté en estado "confirmada" (id = 2)
    if cita.id_estado_cita != 2:
        raise HTTPException(
            status_code=400,
            detail="Solo se puede marcar como presente una cita confirmada"
        )

    # 2. Actualizar estado a "paciente_presente" (id = 9)
    cita.id_estado_cita = 9
    session.add(cita)
    session.commit()
    session.refresh(cita)

    # 3. Crear notificación para el psicólogo
    try:
        from app.models import Paciente, Psicologo

        paciente = session.get(Paciente, cita.id_paciente)
        psicologo = session.get(Psicologo, cita.id_empleado)

        if paciente and psicologo:
            notificacion = Notificacion(
                id_usuario=psicologo.id_usuario,
                id_cita=cita.id_cita,
                tipo_notificacion="cita_paciente_presente",
                asunto="Paciente presente en sala de espera",
                contenido=f"El paciente {paciente.nombres} {paciente.apellido_paterno} ha llegado para su cita de las {cita.hora_inicio.strftime('%H:%M')}",
                estado="pendiente"
            )
            session.add(notificacion)
            session.commit()
    except Exception as e:
        # Si falla la notificación, no afecta el cambio de estado
        print(f"Error al crear notificación: {e}")

    return {
        "message": "Paciente marcado como presente exitosamente",
        "id_cita": cita.id_cita,
        "estado": "paciente_presente"
    }


@router.put("/{id}/iniciar-sesion", response_model=dict)
def iniciar_sesion_cita(session: SessionDep, id: int) -> Any:
    """
    PUT /api/citas/{id}/iniciar-sesion

    Endpoint para que el psicólogo marque que la sesión ha comenzado.

    Lógica:
    1. Actualizar estado de "paciente_presente" a "en_curso" (id_estado_cita = 3)
    2. Registrar el momento en que comenzó la sesión

    Respuesta: confirmación con id_cita y nuevo estado
    """
    # 1. Buscar cita
    cita = session.get(Cita, id)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    # Verificar que esté en estado "paciente_presente" (id = 9)
    if cita.id_estado_cita != 9:
        raise HTTPException(
            status_code=400,
            detail="Solo se puede iniciar sesión cuando el paciente está presente"
        )

    # 2. Actualizar estado a "en_curso" (id = 3)
    cita.id_estado_cita = 3
    cita.fecha_modificacion = datetime.utcnow()
    session.add(cita)
    session.commit()
    session.refresh(cita)

    return {
        "message": "Sesión iniciada exitosamente",
        "id_cita": cita.id_cita,
        "estado": "en_curso"
    }


@router.put("/{id}/completar", response_model=dict)
def completar_cita(session: SessionDep, id: int) -> Any:
    """
    PUT /api/citas/{id}/completar

    Endpoint para que el psicólogo marque la cita como completada.

    Lógica:
    1. Actualizar estado de "en_curso" a "completada" (id_estado_cita = 4)
    2. Registrar el momento en que finalizó la sesión

    Respuesta: confirmación con id_cita y nuevo estado
    """
    # 1. Buscar cita
    cita = session.get(Cita, id)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    # Verificar que esté en estado "en_curso" (id = 3)
    if cita.id_estado_cita != 3:
        raise HTTPException(
            status_code=400,
            detail="Solo se puede completar una cita que está en curso"
        )

    # 2. Actualizar estado a "completada" (id = 4)
    cita.id_estado_cita = 4
    cita.fecha_modificacion = datetime.utcnow()
    session.add(cita)
    session.commit()
    session.refresh(cita)

    return {
        "message": "Cita completada exitosamente",
        "id_cita": cita.id_cita,
        "estado": "completada"
    }
