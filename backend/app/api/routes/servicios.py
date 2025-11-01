from typing import Any

from fastapi import APIRouter
from sqlmodel import select

from app.api.deps import SessionDep
from app.models import Servicio, ServicioPublic, ServiciosPublic

router = APIRouter(prefix="/servicios", tags=["servicios"])


@router.get("/", response_model=list[ServicioPublic])
def get_servicios(session: SessionDep) -> Any:
    """
    GET /api/servicios

    Retorna lista de todos los servicios disponibles de la clínica.

    Respuesta: array de objetos con id_servicio, nombre_servicio, descripcion,
    duracion_minutos, precio, tipo_servicio, estado
    """
    statement = select(Servicio).where(Servicio.estado == 'activo')
    servicios = session.exec(statement).all()

    return servicios
