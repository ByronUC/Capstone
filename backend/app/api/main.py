from fastapi import APIRouter

from app.api.routes import (
    items,
    login,
    private,
    users,
    utils,
    pacientes,
    citas,
    tratamientos,
    medicacion,
    seguimiento,
)
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)

# Módulos clínicos
api_router.include_router(pacientes.router)
api_router.include_router(citas.router)
api_router.include_router(tratamientos.router)
api_router.include_router(medicacion.router)
api_router.include_router(seguimiento.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
