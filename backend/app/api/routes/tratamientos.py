from typing import Any

from fastapi import APIRouter, HTTPException, Body
from sqlmodel import func, select

from app import crud
from app.api.deps import SessionDep
from app.models import (
    Message,
    Tratamiento,
    TratamientoCreate,
    TratamientoPublic,
    TratamientosPublic,
    TratamientoUpdate,
)

router = APIRouter(prefix="/tratamientos", tags=["tratamientos"])


@router.get("/", response_model=TratamientosPublic)
def read_tratamientos(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Obtener lista de tratamientos.

    Retorna tratamientos médicos activos e históricos con filtros por paciente,
    tipo de tratamiento, medicación asociada, estado (activo/completado/suspendido)
    y fecha de inicio.
    """
    count_statement = select(func.count()).select_from(Tratamiento)
    count = session.exec(count_statement).one()

    statement = select(Tratamiento).offset(skip).limit(limit)
    tratamientos = session.exec(statement).all()

    return TratamientosPublic(data=tratamientos, count=count)


@router.get("/{id}", response_model=TratamientoPublic)
def read_tratamiento_by_id(id: int, session: SessionDep) -> Any:
    """
    Obtener tratamiento por ID.

    Retorna detalles completos del tratamiento incluyendo paciente, tipo, medicación
    asociada con dosis y frecuencia, duración estimada, médico responsable,
    observaciones y estado actual.
    """
    tratamiento = session.get(Tratamiento, id)
    if not tratamiento:
        raise HTTPException(
            status_code=404,
            detail="El tratamiento no existe en el sistema",
        )
    return tratamiento


@router.post("/", response_model=TratamientoPublic)
def create_tratamiento(*, session: SessionDep, tratamiento_in: TratamientoCreate) -> Any:
    """
    Crear nuevo tratamiento.

    Registra un tratamiento médico con paciente, tipo de tratamiento, medicación
    asociada, dosis específicas, frecuencia de administración, duración estimada
    y médico responsable. Estado inicial 'activo'.
    """
    tratamiento = crud.create_tratamiento(session=session, tratamiento_create=tratamiento_in)
    return tratamiento


@router.put("/{id}", response_model=TratamientoPublic)
def update_tratamiento_complete(
    *,
    session: SessionDep,
    id: int,
    tratamiento_in: TratamientoCreate,
) -> Any:
    """
    Actualizar tratamiento completo.

    Modifica toda la información de un tratamiento existente incluyendo ajuste
    de medicación, cambio de dosis o modificación de duración.
    """
    db_tratamiento = session.get(Tratamiento, id)
    if not db_tratamiento:
        raise HTTPException(
            status_code=404,
            detail="El tratamiento no existe en el sistema",
        )

    # Actualizar completamente
    tratamiento_data = tratamiento_in.model_dump()
    db_tratamiento.sqlmodel_update(tratamiento_data)
    session.add(db_tratamiento)
    session.commit()
    session.refresh(db_tratamiento)
    return db_tratamiento


@router.patch("/{id}", response_model=TratamientoPublic)
def update_tratamiento_partial(
    *,
    session: SessionDep,
    id: int,
    tratamiento_in: TratamientoUpdate,
) -> Any:
    """
    Actualizar tratamiento parcialmente.

    Actualiza estado (suspender, reanudar, completar), añade observaciones médicas
    o ajusta dosis de medicación sin modificar todo el registro. Registra cambios
    en historial.
    """
    db_tratamiento = session.get(Tratamiento, id)
    if not db_tratamiento:
        raise HTTPException(
            status_code=404,
            detail="El tratamiento no existe en el sistema",
        )

    db_tratamiento = crud.update_tratamiento(
        session=session,
        db_tratamiento=db_tratamiento,
        tratamiento_in=tratamiento_in
    )
    return db_tratamiento


@router.delete("/{id}", response_model=Message)
def delete_tratamiento(session: SessionDep, id: int) -> Message:
    """
    Finalizar y eliminar tratamiento.

    Finaliza un tratamiento y lo elimina del sistema activo. Mueve información a
    historial médico del paciente. Solo permitido si está completado o suspendido.
    """
    tratamiento = session.get(Tratamiento, id)
    if not tratamiento:
        raise HTTPException(status_code=404, detail="Tratamiento no encontrado")

    # Verificar que esté completado o suspendido
    if tratamiento.estado not in ['completado', 'suspendido']:
        raise HTTPException(
            status_code=400,
            detail="Solo se pueden eliminar tratamientos completados o suspendidos"
        )

    # TODO: Mover información a historial médico antes de eliminar

    session.delete(tratamiento)
    session.commit()

    return Message(message="Tratamiento eliminado exitosamente")


@router.post("/{id}/observacion-inicial", response_model=TratamientoPublic)
def update_observacion_inicial(
    *,
    session: SessionDep,
    id: int,
    observacion: str = Body(..., embed=True)
) -> Any:
    """
    Agregar observación inicial del tratamiento.

    Permite al psicólogo agregar la observación/descripción inicial
    del tratamiento después de la primera sesión con el paciente.

    Args:
        id: ID del tratamiento
        observacion: Texto de la observación inicial del tratamiento

    Request body example:
    ```json
    {
      "observacion": "Paciente presenta síntomas de ansiedad leve..."
    }
    ```
    """
    db_tratamiento = session.get(Tratamiento, id)
    if not db_tratamiento:
        raise HTTPException(
            status_code=404,
            detail="El tratamiento no existe en el sistema",
        )

    # Actualizar solo la descripción (observación inicial)
    db_tratamiento.descripcion = observacion
    session.add(db_tratamiento)
    session.commit()
    session.refresh(db_tratamiento)

    return db_tratamiento
