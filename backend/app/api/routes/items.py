import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Message

# NOTA: Este módulo de items es del template original y no se usa en el sistema clínico
# Se mantiene comentado para evitar errores de importación
# TODO: Eliminar completamente o reemplazar con endpoints específicos del sistema clínico

router = APIRouter(prefix="/items", tags=["items"])

# Todas las rutas de items están comentadas porque el modelo Item ya no existe
# Este era parte del template original de FastAPI

# @router.get("/", response_model=ItemsPublic)
# def read_items(
#     session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
# ) -> Any:
#     """
#     Retrieve items.
#     """
#     pass

# @router.get("/{id}", response_model=ItemPublic)
# def read_item(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
#     """
#     Get item by ID.
#     """
#     pass

# @router.post("/", response_model=ItemPublic)
# def create_item(
#     *, session: SessionDep, current_user: CurrentUser, item_in: ItemCreate
# ) -> Any:
#     """
#     Create new item.
#     """
#     pass

# @router.put("/{id}", response_model=ItemPublic)
# def update_item(
#     *,
#     session: SessionDep,
#     current_user: CurrentUser,
#     id: uuid.UUID,
#     item_in: ItemUpdate,
# ) -> Any:
#     """
#     Update an item.
#     """
#     pass

# @router.delete("/{id}")
# def delete_item(
#     session: SessionDep, current_user: CurrentUser, id: uuid.UUID
# ) -> Message:
#     """
#     Delete an item.
#     """
#     pass
