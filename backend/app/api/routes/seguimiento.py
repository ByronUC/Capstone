from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app import crud
from app.api.deps import SessionDep
from app.models import (
    Message,
    Seguimiento,
    SeguimientoCreate,
    SeguimientoPublic,
    SeguimientosPublic,
    SeguimientoUpdate,
)

router = APIRouter(prefix="/seguimiento", tags=["seguimiento"])


@router.get("/", response_model=SeguimientosPublic)
def read_seguimientos(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Obtener registros de seguimiento.

    Retorna registros de seguimiento médico y de servicios con filtros por paciente,
    tipo de seguimiento (post-tratamiento/control/preventivo), fecha, responsable
    o estado del paciente.
    """
    count_statement = select(func.count()).select_from(Seguimiento)
    count = session.exec(count_statement).one()

    statement = select(Seguimiento).offset(skip).limit(limit)
    seguimientos = session.exec(statement).all()

    return SeguimientosPublic(data=seguimientos, count=count)


@router.get("/{id}", response_model=SeguimientoPublic)
def read_seguimiento_by_id(id: int, session: SessionDep) -> Any:
    """
    Obtener seguimiento por ID.

    Retorna detalles completos de un registro de seguimiento específico incluyendo
    paciente, tipo, fecha, observaciones médicas, evolución del estado, próxima
    cita recomendada y responsable.
    """
    seguimiento = session.get(Seguimiento, id)
    if not seguimiento:
        raise HTTPException(
            status_code=404,
            detail="El seguimiento no existe en el sistema",
        )
    return seguimiento


@router.post("/", response_model=SeguimientoPublic)
def create_seguimiento(*, session: SessionDep, seguimiento_in: SeguimientoCreate) -> Any:
    """
    Crear registro de seguimiento.

    Crea un nuevo registro de seguimiento con paciente, tipo de seguimiento,
    observaciones sobre evolución del estado, recomendaciones médicas, próxima
    fecha de control y responsable del seguimiento.
    """
    seguimiento = crud.create_seguimiento(session=session, seguimiento_create=seguimiento_in)
    return seguimiento


@router.put("/{id}", response_model=SeguimientoPublic)
def update_seguimiento_complete(
    *,
    session: SessionDep,
    id: int,
    seguimiento_in: SeguimientoCreate,
) -> Any:
    """
    Actualizar seguimiento completo.

    Modifica completamente un registro de seguimiento incluyendo observaciones,
    recomendaciones y reprogramación de próximo control.
    """
    db_seguimiento = session.get(Seguimiento, id)
    if not db_seguimiento:
        raise HTTPException(
            status_code=404,
            detail="El seguimiento no existe en el sistema",
        )

    # Actualizar completamente
    seguimiento_data = seguimiento_in.model_dump()
    db_seguimiento.sqlmodel_update(seguimiento_data)
    session.add(db_seguimiento)
    session.commit()
    session.refresh(db_seguimiento)
    return db_seguimiento


@router.patch("/{id}", response_model=SeguimientoPublic)
def update_seguimiento_partial(
    *,
    session: SessionDep,
    id: int,
    seguimiento_in: SeguimientoUpdate,
) -> Any:
    """
    Actualizar seguimiento parcialmente.

    Añade nuevas observaciones médicas, actualiza estado del paciente o reprograma
    próxima cita sin modificar todo el registro histórico.
    """
    db_seguimiento = session.get(Seguimiento, id)
    if not db_seguimiento:
        raise HTTPException(
            status_code=404,
            detail="El seguimiento no existe en el sistema",
        )

    db_seguimiento = crud.update_seguimiento(
        session=session,
        db_seguimiento=db_seguimiento,
        seguimiento_in=seguimiento_in
    )
    return db_seguimiento


@router.delete("/{id}", response_model=Message)
def delete_seguimiento(session: SessionDep, id: int) -> Message:
    """
    Eliminar registro de seguimiento.

    Elimina un registro de seguimiento del sistema. Solo permitido si fue creado
    por error y no tiene registros dependientes.
    """
    seguimiento = session.get(Seguimiento, id)
    if not seguimiento:
        raise HTTPException(status_code=404, detail="Seguimiento no encontrado")

    # TODO: Verificar que no tenga registros dependientes

    session.delete(seguimiento)
    session.commit()

    return Message(message="Seguimiento eliminado exitosamente")
