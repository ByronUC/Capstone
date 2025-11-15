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
    servicios,
    psicologos,
    previsiones,
    ciudades,
    salas,
)
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)

# Sistema de Reservas - Core
api_router.include_router(servicios.router)
api_router.include_router(psicologos.router)
api_router.include_router(citas.router)

# Módulos clínicos complementarios
api_router.include_router(pacientes.router)
api_router.include_router(tratamientos.router)
api_router.include_router(medicacion.router)
api_router.include_router(seguimiento.router)

# Módulos de datos maestros
api_router.include_router(previsiones.router)
api_router.include_router(ciudades.router)
api_router.include_router(salas.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
