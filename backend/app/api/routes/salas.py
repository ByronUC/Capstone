from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app import crud
from app.api.deps import SessionDep
from app.models import (
    Message,
    SalaAtencion,
    SalaAtencionCreate,
    SalaAtencionPublic,
    SalasAtencionPublic,
    SalaAtencionUpdate,
)

router = APIRouter(prefix="/salas", tags=["salas"])


@router.get("/", response_model=SalasAtencionPublic)
def read_salas(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Obtener lista de salas de atención.

    Retorna todas las salas registradas en el sistema con su información
    de ubicación, capacidad, equipamiento y estado de disponibilidad.
    """
    count_statement = select(func.count()).select_from(SalaAtencion)
    count = session.exec(count_statement).one()

    statement = select(SalaAtencion).offset(skip).limit(limit)
    salas = session.exec(statement).all()

    return SalasAtencionPublic(data=salas, count=count)


@router.get("/{id}", response_model=SalaAtencionPublic)
def read_sala_by_id(id: int, session: SessionDep) -> Any:
    """
    Obtener sala por ID.

    Retorna los detalles completos de una sala específica incluyendo
    nombre, ubicación, capacidad, equipamiento disponible y estado actual.
    """
    sala = session.get(SalaAtencion, id)
    if not sala:
        raise HTTPException(
            status_code=404,
            detail="La sala no existe en el sistema",
        )
    return sala


@router.post("/", response_model=SalaAtencionPublic)
def create_sala(*, session: SessionDep, sala_in: SalaAtencionCreate) -> Any:
    """
    Crear nueva sala de atención.

    Registra una nueva sala en el sistema con su nombre, ubicación,
    capacidad, equipamiento disponible y estado inicial.
    """
    sala = crud.create_sala_atencion(session=session, sala_create=sala_in)
    return sala


@router.put("/{id}", response_model=SalaAtencionPublic)
def update_sala_complete(
    *,
    session: SessionDep,
    id: int,
    sala_in: SalaAtencionCreate,
) -> Any:
    """
    Actualizar sala completamente.

    Modifica todos los datos de una sala existente incluyendo nombre,
    ubicación, capacidad, equipamiento y estado de disponibilidad.
    """
    db_sala = session.get(SalaAtencion, id)
    if not db_sala:
        raise HTTPException(
            status_code=404,
            detail="La sala no existe en el sistema",
        )

    # Actualizar completamente
    sala_data = sala_in.model_dump()
    db_sala.sqlmodel_update(sala_data)
    session.add(db_sala)
    session.commit()
    session.refresh(db_sala)
    return db_sala


@router.patch("/{id}", response_model=SalaAtencionPublic)
def update_sala_partial(
    *,
    session: SessionDep,
    id: int,
    sala_in: SalaAtencionUpdate,
) -> Any:
    """
    Actualizar sala parcialmente.

    Modifica solo los campos especificados de una sala, como cambiar
    su estado de disponibilidad o actualizar el equipamiento.
    """
    db_sala = session.get(SalaAtencion, id)
    if not db_sala:
        raise HTTPException(
            status_code=404,
            detail="La sala no existe en el sistema",
        )

    db_sala = crud.update_sala_atencion(
        session=session,
        db_sala=db_sala,
        sala_in=sala_in
    )
    return db_sala


@router.delete("/{id}", response_model=Message)
def delete_sala(session: SessionDep, id: int) -> Message:
    """
    Eliminar sala de atención.

    Elimina una sala del sistema. Solo permitido si la sala no tiene
    citas activas o programadas.
    """
    sala = session.get(SalaAtencion, id)
    if not sala:
        raise HTTPException(status_code=404, detail="Sala no encontrada")

    # TODO: Verificar que no tenga citas activas o programadas

    session.delete(sala)
    session.commit()

    return Message(message="Sala eliminada exitosamente")
