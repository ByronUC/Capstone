from typing import Any
from datetime import date, time, datetime, timedelta
import logging

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlmodel import select, func

from app.api.deps import SessionDep, get_current_active_superuser
from app.models import (
    Psicologo,
    PsicologoPublic,
    PsicologosPublic,
    PsicologoCreate,
    PsicologoUpdate,
    PsicologoEspecialidad,
    HorarioDisponible,
    Cita,
    Usuario,
    Message,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/empleados", tags=["empleados"])


@router.get("/disponibles", response_model=list[PsicologoPublic])
def get_psicologos_disponibles(
    session: SessionDep,
    especialidad_id: int | None = Query(None, description="ID de la especialidad")
) -> Any:
    """
    GET /api/psicologos/disponibles?especialidad_id={id}

    Retorna psicólogos que ofrecen esa especialidad.

    Respuesta: array con id_psicologo, nombres, apellidos, especialidades
    """
    if especialidad_id:
        # Buscar psicólogos con esa especialidad
        statement = (
            select(Psicologo)
            .join(PsicologoEspecialidad)
            .where(
                PsicologoEspecialidad.id_especialidad == especialidad_id,
                PsicologoEspecialidad.vigente == True,
                Psicologo.estado == 'activo'
            )
        )
    else:
        # Retornar todos los psicólogos activos
        statement = select(Psicologo).where(Psicologo.estado == 'activo')

    psicologos = session.exec(statement).all()

    return psicologos


from pydantic import BaseModel

class HorarioDisponibilidadInfo(BaseModel):
    """Información de disponibilidad de un horario"""
    hora: str
    disponible: bool
    ocupado: bool  # Si ya tiene una cita programada
    pasado: bool  # Si el horario ya pasó (solo para el día actual)

@router.get("/disponibilidad", response_model=list[HorarioDisponibilidadInfo])
def get_disponibilidad(
    session: SessionDep,
    psicologo_id: int = Query(..., description="ID del psicólogo"),
    fecha: date = Query(..., description="Fecha en formato YYYY-MM-DD")
) -> Any:
    """
    GET /api/disponibilidad?psicologo_id={id}&fecha={YYYY-MM-DD}

    Calcula y retorna horarios con su estado de disponibilidad.

    Lógica:
    1. Consultar tabla horarios_disponibles del psicólogo para ese día de semana
    2. Generar array de horarios posibles (intervalos de 1 hora)
    3. Consultar tabla citas para ver horarios ya ocupados en esa fecha
    4. Marcar horarios como ocupados, pasados o disponibles

    Respuesta: array de objetos con {hora, disponible, ocupado, pasado}
    """
    logger.info(f"===== INICIO get_disponibilidad psicologo_id={psicologo_id}, fecha={fecha} =====")

    # Verificar que el psicólogo existe
    psicologo = session.get(Psicologo, psicologo_id)
    if not psicologo:
        raise HTTPException(status_code=404, detail="Psicólogo no encontrado")

    # Obtener el día de la semana (en minúsculas, sin tildes, como en BD)
    dias_semana = {
        0: "lunes",
        1: "martes",
        2: "miercoles",
        3: "jueves",
        4: "viernes",
        5: "sabado",
        6: "domingo"
    }
    dia_semana = dias_semana[fecha.weekday()]
    logger.info(f"Día de la semana: {dia_semana}")

    # 1. Consultar horarios disponibles del psicólogo para ese día
    statement = select(HorarioDisponible).where(
        HorarioDisponible.id_empleado == psicologo_id,
        HorarioDisponible.dia_semana == dia_semana,
        HorarioDisponible.disponible == True
    )
    horarios_config = session.exec(statement).all()
    logger.info(f"Horarios encontrados en BD: {len(horarios_config)}")

    if not horarios_config:
        logger.warning(f"NO HAY HORARIOS para psicologo {psicologo_id} en {dia_semana}")
        return []  # No hay horarios configurados para este día

    logger.info(f"Generando horarios para {len(horarios_config)} configuraciones")

    # 2. Generar array de horarios posibles (intervalos de 1 hora)
    horarios_disponibles = []
    for config in horarios_config:
        # Validar si el horario está dentro del rango de fechas (si está configurado)
        if config.fecha_desde and fecha < config.fecha_desde:
            continue
        if config.fecha_hasta and fecha > config.fecha_hasta:
            continue

        # Generar horarios desde hora_inicio hasta hora_fin
        hora_actual = datetime.combine(fecha, config.hora_inicio)
        hora_fin = datetime.combine(fecha, config.hora_fin)

        while hora_actual < hora_fin:
            horarios_disponibles.append(hora_actual.time())
            hora_actual += timedelta(hours=1)

    # 3. Consultar citas ya ocupadas en esa fecha
    statement = select(Cita).where(
        Cita.id_empleado == psicologo_id,
        Cita.fecha_cita == fecha,
        Cita.id_estado_cita.in_([1, 2, 3])  # Pendiente, Confirmada, Realizada
    )
    citas_ocupadas = session.exec(statement).all()

    # 4. Identificar horarios ocupados
    horarios_ocupados = set()
    for cita in citas_ocupadas:
        # Marcar como ocupados todos los horarios entre hora_inicio y hora_fin
        hora_actual = datetime.combine(fecha, cita.hora_inicio)
        hora_fin_cita = datetime.combine(fecha, cita.hora_fin)

        while hora_actual < hora_fin_cita:
            horarios_ocupados.add(hora_actual.time())
            hora_actual += timedelta(hours=1)

    # 5. Determinar fecha y hora actual en Chile
    # Usar zoneinfo (disponible en Python 3.9+) para manejar correctamente la zona horaria
    from zoneinfo import ZoneInfo

    chile_tz = ZoneInfo('America/Santiago')
    now_chile = datetime.now(chile_tz)
    fecha_actual_chile = now_chile.date()
    hora_actual_chile = now_chile.time()

    es_hoy = (fecha == fecha_actual_chile)
    logger.info(f"Es hoy: {es_hoy}, Fecha consulta: {fecha}, Fecha actual Chile: {fecha_actual_chile}")
    if es_hoy:
        logger.info(f"Hora actual Chile: {hora_actual_chile}")

    # 6. Generar array con información completa de disponibilidad
    horarios_info = []
    for hora in sorted(set(horarios_disponibles)):
        es_ocupado = hora in horarios_ocupados
        # Un horario está pasado si es hoy Y la hora del slot ya pasó
        es_pasado = es_hoy and hora < hora_actual_chile
        es_disponible = not es_ocupado and not es_pasado

        horarios_info.append(HorarioDisponibilidadInfo(
            hora=hora.strftime("%H:%M"),
            disponible=es_disponible,
            ocupado=es_ocupado,
            pasado=es_pasado
        ))

    logger.info(f"Retornando {len(horarios_info)} horarios con su estado")
    return horarios_info


# ==================== CRUD ENDPOINTS ====================

@router.get("/", dependencies=[Depends(get_current_active_superuser)], response_model=PsicologosPublic)
def get_all_psicologos(
    session: SessionDep,
    skip: int = Query(0, description="Número de registros a saltar"),
    limit: int = Query(100, description="Límite de registros a retornar")
) -> Any:
    """
    Obtener lista de todos los empleados (solo admin).

    Parámetros:
    - skip: Paginación - registros a saltar
    - limit: Paginación - máximo de registros a retornar

    Retorna: Lista de empleados con conteo total
    """
    # Contar total de psicólogos
    count_statement = select(func.count()).select_from(Psicologo)
    count = session.exec(count_statement).one()

    # Obtener psicólogos con paginación
    statement = select(Psicologo).offset(skip).limit(limit).order_by(Psicologo.id_empleado.desc())
    psicologos = session.exec(statement).all()

    return PsicologosPublic(data=psicologos, count=count)


@router.get("/{empleado_id}", dependencies=[Depends(get_current_active_superuser)], response_model=PsicologoPublic)
def get_psicologo_by_id(
    session: SessionDep,
    empleado_id: int
) -> Any:
    """
    Obtener un empleado por ID (solo admin).
    """
    psicologo = session.get(Psicologo, empleado_id)
    if not psicologo:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    return psicologo


@router.post("/", dependencies=[Depends(get_current_active_superuser)], response_model=PsicologoPublic)
def create_psicologo(
    session: SessionDep,
    psicologo_in: PsicologoCreate
) -> Any:
    """
    Crear un nuevo empleado (solo admin).

    Nota: El id_usuario debe existir previamente en la tabla usuarios.

    Roles disponibles (id_rol):
    - 1: administrador - Acceso completo al sistema
    - 2: psicologo - Profesional de salud mental
    - 3: recepcionista - Personal administrativo y atención al cliente
    - 4: supervisor - Supervisor clínico con acceso a reportes
    """
    # Verificar que el usuario existe
    usuario = session.get(Usuario, psicologo_in.id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Verificar que el usuario no esté ya asociado a otro empleado
    existing_psicologo = session.exec(
        select(Psicologo).where(Psicologo.id_usuario == psicologo_in.id_usuario)
    ).first()
    if existing_psicologo:
        raise HTTPException(
            status_code=400,
            detail="Este usuario ya está asociado a un empleado"
        )

    # Verificar que el RUT no esté duplicado
    existing_rut = session.exec(
        select(Psicologo).where(Psicologo.rut == psicologo_in.rut)
    ).first()
    if existing_rut:
        raise HTTPException(status_code=400, detail="El RUT ya está registrado")

    # Verificar que el registro profesional no esté duplicado
    existing_registro = session.exec(
        select(Psicologo).where(Psicologo.registro_profesional == psicologo_in.registro_profesional)
    ).first()
    if existing_registro:
        raise HTTPException(
            status_code=400,
            detail="El registro profesional ya está registrado"
        )

    # Crear el psicólogo
    psicologo = Psicologo.model_validate(psicologo_in)
    session.add(psicologo)
    session.commit()
    session.refresh(psicologo)

    return psicologo


@router.put("/{empleado_id}", dependencies=[Depends(get_current_active_superuser)], response_model=PsicologoPublic)
def update_psicologo_complete(
    session: SessionDep,
    empleado_id: int,
    psicologo_in: PsicologoCreate
) -> Any:
    """
    Actualizar un empleado completamente (todos los campos requeridos) (solo admin).

    Roles disponibles (id_rol):
    - 1: administrador - Acceso completo al sistema
    - 2: psicologo - Profesional de salud mental
    - 3: recepcionista - Personal administrativo y atención al cliente
    - 4: supervisor - Supervisor clínico con acceso a reportes
    """
    psicologo = session.get(Psicologo, empleado_id)
    if not psicologo:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    # Verificar RUT duplicado
    if psicologo_in.rut != psicologo.rut:
        existing_rut = session.exec(
            select(Psicologo).where(
                Psicologo.rut == psicologo_in.rut,
                Psicologo.id_empleado != empleado_id
            )
        ).first()
        if existing_rut:
            raise HTTPException(status_code=400, detail="El RUT ya está registrado")

    # Verificar registro profesional duplicado
    if psicologo_in.registro_profesional != psicologo.registro_profesional:
        existing_registro = session.exec(
            select(Psicologo).where(
                Psicologo.registro_profesional == psicologo_in.registro_profesional,
                Psicologo.id_empleado != empleado_id
            )
        ).first()
        if existing_registro:
            raise HTTPException(
                status_code=400,
                detail="El registro profesional ya está registrado"
            )

    # Verificar que el id_usuario no esté asociado a otro empleado
    if psicologo_in.id_usuario != psicologo.id_usuario:
        existing_psicologo = session.exec(
            select(Psicologo).where(
                Psicologo.id_usuario == psicologo_in.id_usuario,
                Psicologo.id_empleado != empleado_id
            )
        ).first()
        if existing_psicologo:
            raise HTTPException(
                status_code=400,
                detail="Este usuario ya está asociado a otro empleado"
            )

    # Actualizar completamente
    psicologo_data = psicologo_in.model_dump()
    psicologo.sqlmodel_update(psicologo_data)
    session.add(psicologo)
    session.commit()
    session.refresh(psicologo)

    return psicologo


@router.patch("/{empleado_id}", dependencies=[Depends(get_current_active_superuser)], response_model=PsicologoPublic)
def update_psicologo_partial(
    session: SessionDep,
    empleado_id: int,
    psicologo_in: PsicologoUpdate
) -> Any:
    """
    Actualizar un empleado parcialmente (solo campos proporcionados) (solo admin).

    Roles disponibles (id_rol):
    - 1: administrador - Acceso completo al sistema
    - 2: psicologo - Profesional de salud mental
    - 3: recepcionista - Personal administrativo y atención al cliente
    - 4: supervisor - Supervisor clínico con acceso a reportes
    """
    psicologo = session.get(Psicologo, empleado_id)
    if not psicologo:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    # Verificar RUT duplicado (si se está actualizando)
    if psicologo_in.rut and psicologo_in.rut != psicologo.rut:
        existing_rut = session.exec(
            select(Psicologo).where(
                Psicologo.rut == psicologo_in.rut,
                Psicologo.id_empleado != empleado_id
            )
        ).first()
        if existing_rut:
            raise HTTPException(status_code=400, detail="El RUT ya está registrado")

    # Verificar registro profesional duplicado (si se está actualizando)
    if psicologo_in.registro_profesional and psicologo_in.registro_profesional != psicologo.registro_profesional:
        existing_registro = session.exec(
            select(Psicologo).where(
                Psicologo.registro_profesional == psicologo_in.registro_profesional,
                Psicologo.id_empleado != empleado_id
            )
        ).first()
        if existing_registro:
            raise HTTPException(
                status_code=400,
                detail="El registro profesional ya está registrado"
            )

    # Actualizar campos
    psicologo_data = psicologo_in.model_dump(exclude_unset=True)
    psicologo.sqlmodel_update(psicologo_data)
    session.add(psicologo)
    session.commit()
    session.refresh(psicologo)

    return psicologo


@router.delete("/{empleado_id}", dependencies=[Depends(get_current_active_superuser)], response_model=Message)
def delete_psicologo(
    session: SessionDep,
    empleado_id: int
) -> Any:
    """
    Eliminar un empleado (solo admin).

    Nota: Esto hará un soft delete cambiando el estado a 'inactivo'.
    """
    psicologo = session.get(Psicologo, empleado_id)
    if not psicologo:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    # Soft delete
    psicologo.estado = 'inactivo'
    session.add(psicologo)
    session.commit()

    return Message(message="Empleado eliminado correctamente")
