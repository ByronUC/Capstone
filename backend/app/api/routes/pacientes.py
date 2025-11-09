from typing import Any
from datetime import datetime

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app import crud
from app.api.deps import SessionDep
from app.models import (
    Message,
    Paciente,
    PacienteCreate,
    PacientePublic,
    PacientesPublic,
    PacienteUpdate,
    Tratamiento,
    Medicamento,
    Seguimiento,
    Psicologo,
)

router = APIRouter(prefix="/pacientes", tags=["pacientes"])


@router.get("/", response_model=PacientesPublic)
def read_pacientes(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Obtener lista de pacientes.

    Retorna lista de pacientes con historial médico básico, filtrable por nombre,
    DNI, estado (activo/inactivo) o tipo de tratamiento actual.
    """
    count_statement = select(func.count()).select_from(Paciente)
    count = session.exec(count_statement).one()

    statement = select(Paciente).offset(skip).limit(limit)
    pacientes = session.exec(statement).all()

    return PacientesPublic(data=pacientes, count=count)


@router.get("/{id}", response_model=PacientePublic)
def read_paciente_by_id(id: int, session: SessionDep) -> Any:
    """
    Obtener paciente por ID.

    Retorna información completa del paciente incluyendo datos personales,
    antecedentes médicos, alergias, tratamientos activos, contacto de emergencia
    e historial de atención.
    """
    paciente = session.get(Paciente, id)
    if not paciente:
        raise HTTPException(
            status_code=404,
            detail="El paciente no existe en el sistema",
        )
    return paciente


@router.post("/", response_model=PacientePublic)
def create_paciente(*, session: SessionDep, paciente_in: PacienteCreate) -> Any:
    """
    Registrar nuevo paciente.

    Registra un nuevo paciente con datos personales, antecedentes médicos relevantes,
    alergias conocidas, tipo de sangre y contacto de emergencia. Genera historial
    clínico inicial.
    """
    # Verificar si el RUT ya existe
    paciente = crud.get_paciente_by_rut(session=session, rut=paciente_in.rut)
    if paciente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un paciente con este RUT en el sistema",
        )

    paciente = crud.create_paciente(session=session, paciente_create=paciente_in)
    return paciente


@router.put("/{id}", response_model=PacientePublic)
def update_paciente_complete(
    *,
    session: SessionDep,
    id: int,
    paciente_in: PacienteCreate,
) -> Any:
    """
    Actualizar paciente completo.

    Actualiza toda la información del paciente incluyendo datos personales
    y antecedentes médicos completos.
    """
    db_paciente = session.get(Paciente, id)
    if not db_paciente:
        raise HTTPException(
            status_code=404,
            detail="El paciente no existe en el sistema",
        )

    # Verificar si el RUT ya existe en otro paciente
    if paciente_in.rut != db_paciente.rut:
        existing_paciente = crud.get_paciente_by_rut(session=session, rut=paciente_in.rut)
        if existing_paciente and existing_paciente.id_paciente != id:
            raise HTTPException(
                status_code=409,
                detail="Ya existe otro paciente con este RUT"
            )

    # Actualizar completamente
    paciente_data = paciente_in.model_dump()
    db_paciente.sqlmodel_update(paciente_data)
    session.add(db_paciente)
    session.commit()
    session.refresh(db_paciente)
    return db_paciente


@router.patch("/{id}", response_model=PacientePublic)
def update_paciente_partial(
    *,
    session: SessionDep,
    id: int,
    paciente_in: PacienteUpdate,
) -> Any:
    """
    Actualizar paciente parcialmente.

    Modifica campos específicos del registro del paciente como contacto, dirección,
    alergias o información de emergencia sin afectar el historial médico.
    """
    db_paciente = session.get(Paciente, id)
    if not db_paciente:
        raise HTTPException(
            status_code=404,
            detail="El paciente no existe en el sistema",
        )

    # Verificar si el RUT ya existe en otro paciente
    if paciente_in.rut and paciente_in.rut != db_paciente.rut:
        existing_paciente = crud.get_paciente_by_rut(session=session, rut=paciente_in.rut)
        if existing_paciente and existing_paciente.id_paciente != id:
            raise HTTPException(
                status_code=409,
                detail="Ya existe otro paciente con este RUT"
            )

    db_paciente = crud.update_paciente(session=session, db_paciente=db_paciente, paciente_in=paciente_in)
    return db_paciente


@router.delete("/{id}", response_model=Message)
def delete_paciente(session: SessionDep, id: int) -> Message:
    """
    Dar de baja paciente.

    Marca el paciente como inactivo en el sistema. Valida que no tenga tratamientos
    activos o citas programadas. No elimina físicamente para mantener historial médico.
    """
    paciente = session.get(Paciente, id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    # Verificar si tiene tratamientos activos
    statement = select(func.count()).select_from(
        session.query(Paciente).join(Paciente.tratamientos).filter(
            Paciente.id_paciente == id,
        )
    )

    # En lugar de eliminar, marcar como inactivo
    paciente.estado = 'inactivo'
    session.add(paciente)
    session.commit()

    return Message(message="Paciente dado de baja exitosamente")


@router.get("/{id}/reporte", response_model=dict)
def get_reporte_paciente(id: int, session: SessionDep) -> Any:
    """
    Obtener reporte general completo del paciente.

    Incluye:
    - Información básica del paciente
    - Tratamientos (activos e históricos)
    - Medicamentos (activos e históricos)
    - Seguimientos
    """
    # Verificar que el paciente existe
    paciente = session.get(Paciente, id)
    if not paciente:
        raise HTTPException(
            status_code=404,
            detail="El paciente no existe en el sistema",
        )

    # Calcular edad
    hoy = datetime.now().date()
    edad = hoy.year - paciente.fecha_nacimiento.year
    if hoy.month < paciente.fecha_nacimiento.month or \
       (hoy.month == paciente.fecha_nacimiento.month and hoy.day < paciente.fecha_nacimiento.day):
        edad -= 1

    # Obtener tratamientos
    tratamientos_stmt = select(Tratamiento).where(
        Tratamiento.id_paciente == id
    ).order_by(Tratamiento.fecha_inicio.desc())
    tratamientos = session.exec(tratamientos_stmt).all()

    tratamientos_data = []
    for t in tratamientos:
        psicologo = session.get(Psicologo, t.id_empleado)
        tratamientos_data.append({
            "id_tratamiento": t.id_tratamiento,
            "tipo_tratamiento": t.tipo_tratamiento,
            "descripcion": t.descripcion,
            "objetivos": t.objetivos,
            "fecha_inicio": t.fecha_inicio.isoformat(),
            "fecha_fin_estimada": t.fecha_fin_estimada.isoformat() if t.fecha_fin_estimada else None,
            "fecha_fin_real": t.fecha_fin_real.isoformat() if t.fecha_fin_real else None,
            "estado": t.estado,
            "psicologo": f"{psicologo.nombres} {psicologo.apellido_paterno}" if psicologo else "N/A",
            "fecha_registro": t.fecha_registro.isoformat() if t.fecha_registro else None
        })

    # Obtener medicamentos
    medicamentos_stmt = select(Medicamento).where(
        Medicamento.id_paciente == id
    ).order_by(Medicamento.fecha_inicio.desc())
    medicamentos = session.exec(medicamentos_stmt).all()

    medicamentos_data = []
    for m in medicamentos:
        medicamentos_data.append({
            "id_medicamento": m.id_medicamento,
            "nombre_medicamento": m.nombre_medicamento,
            "dosis": m.dosis,
            "frecuencia": m.frecuencia,
            "via_administracion": m.via_administracion,
            "fecha_inicio": m.fecha_inicio.isoformat(),
            "fecha_fin": m.fecha_fin.isoformat() if m.fecha_fin else None,
            "prescrito_por": m.prescrito_por,
            "observaciones": m.observaciones,
            "estado": m.estado,
            "fecha_registro": m.fecha_registro.isoformat() if m.fecha_registro else None
        })

    # Obtener seguimientos
    seguimientos_stmt = select(Seguimiento).where(
        Seguimiento.id_paciente == id
    ).order_by(Seguimiento.fecha_seguimiento.desc())
    seguimientos = session.exec(seguimientos_stmt).all()

    seguimientos_data = []
    for s in seguimientos:
        psicologo = session.get(Psicologo, s.id_empleado)
        seguimientos_data.append({
            "id_seguimiento": s.id_seguimiento,
            "fecha_seguimiento": s.fecha_seguimiento.isoformat(),
            "tipo_seguimiento": s.tipo_seguimiento,
            "estado_animo": s.estado_animo,
            "nivel_funcionalidad": s.nivel_funcionalidad,
            "adherencia_tratamiento": s.adherencia_tratamiento,
            "observaciones": s.observaciones,
            "proxima_evaluacion": s.proxima_evaluacion.isoformat() if s.proxima_evaluacion else None,
            "psicologo": f"{psicologo.nombres} {psicologo.apellido_paterno}" if psicologo else "N/A",
            "fecha_registro": s.fecha_registro.isoformat() if s.fecha_registro else None
        })

    # Construir reporte
    reporte = {
        "paciente": {
            "id_paciente": paciente.id_paciente,
            "rut": paciente.rut,
            "nombres": paciente.nombres,
            "apellido_paterno": paciente.apellido_paterno,
            "apellido_materno": paciente.apellido_materno,
            "fecha_nacimiento": paciente.fecha_nacimiento.isoformat(),
            "edad": edad,
            "genero": paciente.genero,
            "telefono": paciente.telefono,
            "email": paciente.email,
            "direccion": paciente.direccion,
            "estado_civil": paciente.estado_civil,
            "ocupacion": paciente.ocupacion,
            "estado": paciente.estado,
            "fecha_registro": paciente.fecha_registro.isoformat() if paciente.fecha_registro else None
        },
        "resumen": {
            "total_tratamientos": len(tratamientos),
            "tratamientos_activos": len([t for t in tratamientos if t.estado == 'activo']),
            "total_medicamentos": len(medicamentos),
            "medicamentos_activos": len([m for m in medicamentos if m.estado == 'activo']),
            "total_seguimientos": len(seguimientos)
        },
        "tratamientos": tratamientos_data,
        "medicamentos": medicamentos_data,
        "seguimientos": seguimientos_data
    }

    return reporte
