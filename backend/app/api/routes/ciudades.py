from typing import Any

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlmodel import func, select

from app.api.deps import SessionDep, get_current_active_superuser
from app.models import (
    Ciudad,
    CiudadCreate,
    CiudadUpdate,
    CiudadPublic,
    CiudadesPublic,
    Region,
    Message,
)

router = APIRouter(prefix="/ciudades", tags=["ciudades"])


@router.get("/", response_model=CiudadesPublic)
def get_all_ciudades(
    session: SessionDep,
    skip: int = Query(0, description="Número de registros a saltar"),
    limit: int = Query(100, description="Límite de registros a retornar"),
    id_region: int | None = Query(None, description="Filtrar por ID de región")
) -> Any:
    """
    Obtener lista de todas las ciudades.

    Permite filtrar por región usando el parámetro id_region.
    """
    # Construir statement base
    statement = select(Ciudad)

    # Filtrar por región si se proporciona
    if id_region is not None:
        statement = statement.where(Ciudad.id_region == id_region)

    # Contar total de ciudades
    count_statement = select(func.count()).select_from(statement.subquery())
    count = session.exec(count_statement).one()

    # Obtener ciudades con paginación
    statement = statement.offset(skip).limit(limit).order_by(Ciudad.nombre_ciudad)
    ciudades = session.exec(statement).all()

    return CiudadesPublic(data=ciudades, count=count)


@router.get("/{ciudad_id}", response_model=CiudadPublic)
def get_ciudad_by_id(
    session: SessionDep,
    ciudad_id: int
) -> Any:
    """
    Obtener una ciudad por ID.
    """
    ciudad = session.get(Ciudad, ciudad_id)
    if not ciudad:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")

    return ciudad


@router.post("/", dependencies=[Depends(get_current_active_superuser)], response_model=CiudadPublic)
def create_ciudad(
    session: SessionDep,
    ciudad_in: CiudadCreate
) -> Any:
    """
    Crear una nueva ciudad (solo admin).

    Nota: El id_region debe existir previamente en la tabla regiones.
    """
    # Verificar que la región existe
    region = session.get(Region, ciudad_in.id_region)
    if not region:
        raise HTTPException(status_code=404, detail="Región no encontrada")

    # Verificar que no exista una ciudad con el mismo nombre en la misma región
    existing_ciudad = session.exec(
        select(Ciudad).where(
            Ciudad.nombre_ciudad == ciudad_in.nombre_ciudad,
            Ciudad.id_region == ciudad_in.id_region
        )
    ).first()
    if existing_ciudad:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una ciudad con este nombre en la región seleccionada"
        )

    # Crear la ciudad
    ciudad = Ciudad.model_validate(ciudad_in)
    session.add(ciudad)
    session.commit()
    session.refresh(ciudad)

    return ciudad


@router.patch("/{ciudad_id}", dependencies=[Depends(get_current_active_superuser)], response_model=CiudadPublic)
def update_ciudad(
    session: SessionDep,
    ciudad_id: int,
    ciudad_in: CiudadUpdate
) -> Any:
    """
    Actualizar una ciudad existente (solo admin).
    """
    ciudad = session.get(Ciudad, ciudad_id)
    if not ciudad:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")

    # Verificar que la región existe (si se está actualizando)
    if ciudad_in.id_region is not None:
        region = session.get(Region, ciudad_in.id_region)
        if not region:
            raise HTTPException(status_code=404, detail="Región no encontrada")

    # Verificar nombre duplicado en la misma región
    if ciudad_in.nombre_ciudad or ciudad_in.id_region:
        nombre_a_verificar = ciudad_in.nombre_ciudad if ciudad_in.nombre_ciudad else ciudad.nombre_ciudad
        region_a_verificar = ciudad_in.id_region if ciudad_in.id_region is not None else ciudad.id_region

        existing_ciudad = session.exec(
            select(Ciudad).where(
                Ciudad.nombre_ciudad == nombre_a_verificar,
                Ciudad.id_region == region_a_verificar,
                Ciudad.id_ciudad != ciudad_id
            )
        ).first()
        if existing_ciudad:
            raise HTTPException(
                status_code=400,
                detail="Ya existe una ciudad con este nombre en la región seleccionada"
            )

    # Actualizar campos
    ciudad_data = ciudad_in.model_dump(exclude_unset=True)
    ciudad.sqlmodel_update(ciudad_data)
    session.add(ciudad)
    session.commit()
    session.refresh(ciudad)

    return ciudad


@router.delete("/{ciudad_id}", dependencies=[Depends(get_current_active_superuser)], response_model=Message)
def delete_ciudad(
    session: SessionDep,
    ciudad_id: int
) -> Any:
    """
    Eliminar una ciudad (solo admin).

    Nota: No se puede eliminar si tiene pacientes asociados.
    """
    ciudad = session.get(Ciudad, ciudad_id)
    if not ciudad:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")

    # Verificar si tiene pacientes asociados
    if ciudad.pacientes:
        raise HTTPException(
            status_code=400,
            detail=f"No se puede eliminar la ciudad porque tiene {len(ciudad.pacientes)} paciente(s) asociado(s)"
        )

    session.delete(ciudad)
    session.commit()

    return Message(message="Ciudad eliminada correctamente")
