from typing import Any

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlmodel import func, select

from app.api.deps import SessionDep, get_current_active_superuser
from app.models import (
    Prevision,
    PrevisionCreate,
    PrevisionUpdate,
    PrevisionPublic,
    PrevisionesPublic,
    Message,
)

router = APIRouter(prefix="/previsiones", tags=["previsiones"])


@router.get("/", response_model=PrevisionesPublic)
def get_all_previsiones(
    session: SessionDep,
    skip: int = Query(0, description="Número de registros a saltar"),
    limit: int = Query(100, description="Límite de registros a retornar")
) -> Any:
    """
    Obtener lista de todas las previsiones de salud.

    Incluye sistemas públicos (FONASA) y privados (ISAPREs).
    """
    # Contar total de previsiones
    count_statement = select(func.count()).select_from(Prevision)
    count = session.exec(count_statement).one()

    # Obtener previsiones con paginación
    statement = select(Prevision).offset(skip).limit(limit).order_by(Prevision.nombre_prevision)
    previsiones = session.exec(statement).all()

    return PrevisionesPublic(data=previsiones, count=count)


@router.get("/{prevision_id}", response_model=PrevisionPublic)
def get_prevision_by_id(
    session: SessionDep,
    prevision_id: int
) -> Any:
    """
    Obtener una previsión por ID.
    """
    prevision = session.get(Prevision, prevision_id)
    if not prevision:
        raise HTTPException(status_code=404, detail="Previsión no encontrada")

    return prevision


@router.post("/", dependencies=[Depends(get_current_active_superuser)], response_model=PrevisionPublic)
def create_prevision(
    session: SessionDep,
    prevision_in: PrevisionCreate
) -> Any:
    """
    Crear una nueva previsión (solo admin).

    Tipos disponibles:
    - fonasa: FONASA (sistema público)
    - isapre: ISAPRE (sistema privado)
    - particular: Sin previsión (pago particular)
    - otro: Otro tipo de previsión
    """
    # Verificar que el nombre no esté duplicado
    existing_prevision = session.exec(
        select(Prevision).where(Prevision.nombre_prevision == prevision_in.nombre_prevision)
    ).first()
    if existing_prevision:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una previsión con este nombre"
        )

    # Crear la previsión
    prevision = Prevision.model_validate(prevision_in)
    session.add(prevision)
    session.commit()
    session.refresh(prevision)

    return prevision


@router.patch("/{prevision_id}", dependencies=[Depends(get_current_active_superuser)], response_model=PrevisionPublic)
def update_prevision(
    session: SessionDep,
    prevision_id: int,
    prevision_in: PrevisionUpdate
) -> Any:
    """
    Actualizar una previsión existente (solo admin).

    Tipos disponibles:
    - fonasa: FONASA (sistema público)
    - isapre: ISAPRE (sistema privado)
    - particular: Sin previsión (pago particular)
    - otro: Otro tipo de previsión
    """
    prevision = session.get(Prevision, prevision_id)
    if not prevision:
        raise HTTPException(status_code=404, detail="Previsión no encontrada")

    # Verificar nombre duplicado (si se está actualizando)
    if prevision_in.nombre_prevision and prevision_in.nombre_prevision != prevision.nombre_prevision:
        existing_prevision = session.exec(
            select(Prevision).where(
                Prevision.nombre_prevision == prevision_in.nombre_prevision,
                Prevision.id_prevision != prevision_id
            )
        ).first()
        if existing_prevision:
            raise HTTPException(
                status_code=400,
                detail="Ya existe una previsión con este nombre"
            )

    # Actualizar campos
    prevision_data = prevision_in.model_dump(exclude_unset=True)
    prevision.sqlmodel_update(prevision_data)
    session.add(prevision)
    session.commit()
    session.refresh(prevision)

    return prevision


@router.delete("/{prevision_id}", dependencies=[Depends(get_current_active_superuser)], response_model=Message)
def delete_prevision(
    session: SessionDep,
    prevision_id: int
) -> Any:
    """
    Eliminar una previsión (solo admin).

    Nota: No se puede eliminar si tiene pacientes asociados.
    """
    prevision = session.get(Prevision, prevision_id)
    if not prevision:
        raise HTTPException(status_code=404, detail="Previsión no encontrada")

    # Verificar si tiene pacientes asociados
    if prevision.pacientes:
        raise HTTPException(
            status_code=400,
            detail=f"No se puede eliminar la previsión porque tiene {len(prevision.pacientes)} paciente(s) asociado(s)"
        )

    session.delete(prevision)
    session.commit()

    return Message(message="Previsión eliminada correctamente")
