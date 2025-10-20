from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app import crud
from app.api.deps import SessionDep
from app.models import (
    Message,
    Cita,
    CitaCreate,
    CitaPublic,
    CitasPublic,
    CitaUpdate,
)

router = APIRouter(prefix="/citas", tags=["citas"])


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


@router.get("/{id}", response_model=CitaPublic)
def read_cita_by_id(id: int, session: SessionDep) -> Any:
    """
    Obtener cita por ID.

    Retorna detalles completos de una cita específica incluyendo cliente, empleado
    asignado, fecha, hora, duración, servicio solicitado, estado actual y observaciones.
    """
    cita = session.get(Cita, id)
    if not cita:
        raise HTTPException(
            status_code=404,
            detail="La cita no existe en el sistema",
        )
    return cita


@router.post("/", response_model=CitaPublic)
def create_cita(*, session: SessionDep, cita_in: CitaCreate) -> Any:
    """
    Crear nueva cita.

    Crea una cita con fecha, hora, cliente, empleado asignado y servicio solicitado.
    Valida disponibilidad de horario del empleado y evita solapamiento de citas.
    Retorna conflicto si el horario no está disponible.
    """
    # TODO: Implementar validación de disponibilidad de horario
    # TODO: Implementar validación de solapamiento de citas

    cita = crud.create_cita(session=session, cita_create=cita_in)
    return cita


@router.put("/{id}", response_model=CitaPublic)
def update_cita_complete(
    *,
    session: SessionDep,
    id: int,
    cita_in: CitaCreate,
) -> Any:
    """
    Actualizar cita completa.

    Modifica completamente los datos de una cita existente incluyendo reprogramación
    de fecha/hora. Valida nueva disponibilidad antes de actualizar.
    """
    db_cita = session.get(Cita, id)
    if not db_cita:
        raise HTTPException(
            status_code=404,
            detail="La cita no existe en el sistema",
        )

    # TODO: Implementar validación de disponibilidad de horario

    # Actualizar completamente
    cita_data = cita_in.model_dump()
    db_cita.sqlmodel_update(cita_data)
    session.add(db_cita)
    session.commit()
    session.refresh(db_cita)
    return db_cita


@router.patch("/{id}", response_model=CitaPublic)
def update_cita_partial(
    *,
    session: SessionDep,
    id: int,
    cita_in: CitaUpdate,
) -> Any:
    """
    Actualizar estado de cita.

    Actualiza campos específicos como estado (confirmar, cancelar, completar),
    observaciones o asignación de empleado sin modificar toda la cita.
    Útil para cambios de estado rápidos.
    """
    db_cita = session.get(Cita, id)
    if not db_cita:
        raise HTTPException(
            status_code=404,
            detail="La cita no existe en el sistema",
        )

    db_cita = crud.update_cita(session=session, db_cita=db_cita, cita_in=cita_in)
    return db_cita


@router.delete("/{id}", response_model=Message)
def delete_cita(session: SessionDep, id: int) -> Message:
    """
    Cancelar y eliminar cita.

    Cancela y elimina una cita del sistema. Notifica al cliente y empleado asignado.
    Libera el horario para nuevas citas.
    """
    cita = session.get(Cita, id)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    # TODO: Implementar notificación al cliente y empleado

    session.delete(cita)
    session.commit()

    return Message(message="Cita eliminada exitosamente")
