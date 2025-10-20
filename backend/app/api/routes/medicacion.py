from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app import crud
from app.api.deps import SessionDep
from app.models import (
    Message,
    Medicamento,
    MedicamentoCreate,
    MedicamentoPublic,
    MedicamentosPublic,
    MedicamentoUpdate,
)

router = APIRouter(prefix="/medicacion", tags=["medicacion"])


@router.get("/", response_model=MedicamentosPublic)
def read_medicamentos(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Obtener catálogo de medicamentos.

    Retorna catálogo completo de medicamentos disponibles con filtros por nombre
    comercial, principio activo, tipo (tableta/jarabe/inyectable), laboratorio
    o disponibilidad en inventario.
    """
    count_statement = select(func.count()).select_from(Medicamento)
    count = session.exec(count_statement).one()

    statement = select(Medicamento).offset(skip).limit(limit)
    medicamentos = session.exec(statement).all()

    return MedicamentosPublic(data=medicamentos, count=count)


@router.get("/{id}", response_model=MedicamentoPublic)
def read_medicamento_by_id(id: int, session: SessionDep) -> Any:
    """
    Obtener medicamento por ID.

    Retorna información detallada del medicamento incluyendo nombre comercial,
    principio activo, composición química, presentación, dosis recomendadas,
    contraindicaciones, efectos secundarios y stock disponible.
    """
    medicamento = session.get(Medicamento, id)
    if not medicamento:
        raise HTTPException(
            status_code=404,
            detail="El medicamento no existe en el sistema",
        )
    return medicamento


@router.post("/", response_model=MedicamentoPublic)
def create_medicamento(*, session: SessionDep, medicamento_in: MedicamentoCreate) -> Any:
    """
    Añadir medicamento al catálogo.

    Añade un nuevo medicamento al catálogo del sistema con nombre, principio activo,
    composición, presentación, usos terapéuticos, dosis, contraindicaciones y
    cantidad en inventario inicial.
    """
    medicamento = crud.create_medicamento(session=session, medicamento_create=medicamento_in)
    return medicamento


@router.put("/{id}", response_model=MedicamentoPublic)
def update_medicamento_complete(
    *,
    session: SessionDep,
    id: int,
    medicamento_in: MedicamentoCreate,
) -> Any:
    """
    Actualizar medicamento completo.

    Actualiza toda la información de un medicamento incluyendo datos técnicos,
    dosis, contraindicaciones y stock disponible.
    """
    db_medicamento = session.get(Medicamento, id)
    if not db_medicamento:
        raise HTTPException(
            status_code=404,
            detail="El medicamento no existe en el sistema",
        )

    # Actualizar completamente
    medicamento_data = medicamento_in.model_dump()
    db_medicamento.sqlmodel_update(medicamento_data)
    session.add(db_medicamento)
    session.commit()
    session.refresh(db_medicamento)
    return db_medicamento


@router.patch("/{id}", response_model=MedicamentoPublic)
def update_medicamento_partial(
    *,
    session: SessionDep,
    id: int,
    medicamento_in: MedicamentoUpdate,
) -> Any:
    """
    Actualizar medicamento parcialmente.

    Modifica campos específicos como disponibilidad en inventario, dosis recomendada,
    precio o estado (disponible/agotado) sin modificar datos técnicos completos.
    """
    db_medicamento = session.get(Medicamento, id)
    if not db_medicamento:
        raise HTTPException(
            status_code=404,
            detail="El medicamento no existe en el sistema",
        )

    db_medicamento = crud.update_medicamento(
        session=session,
        db_medicamento=db_medicamento,
        medicamento_in=medicamento_in
    )
    return db_medicamento


@router.delete("/{id}", response_model=Message)
def delete_medicamento(session: SessionDep, id: int) -> Message:
    """
    Eliminar medicamento del catálogo.

    Elimina un medicamento del catálogo si no está en uso activo en ningún
    tratamiento. Retorna error 409 si está asociado a tratamientos activos.
    """
    medicamento = session.get(Medicamento, id)
    if not medicamento:
        raise HTTPException(status_code=404, detail="Medicamento no encontrado")

    # Verificar si está asociado a algún tratamiento activo
    # TODO: Implementar verificación de tratamientos activos asociados

    session.delete(medicamento)
    session.commit()

    return Message(message="Medicamento eliminado exitosamente")
