from typing import Any
from datetime import date, time, datetime, timedelta
import logging

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from app.api.deps import SessionDep
from app.models import (
    Psicologo,
    PsicologoPublic,
    PsicologoEspecialidad,
    HorarioDisponible,
    Cita,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/psicologos", tags=["psicologos"])


@router.get("/disponibles", response_model=list[PsicologoPublic])
def get_psicologos_disponibles(
    session: SessionDep,
    especialidad_id: int | None = Query(None, description="ID de la especialidad")
) -> Any:
    """
    GET /api/psicologos/disponibles?especialidad_id={id}

    Retorna psicólogos que ofrecen esa especialidad.

    Respuesta: array con id_psicologo, nombres, apellidos, especialidades
    """
    if especialidad_id:
        # Buscar psicólogos con esa especialidad
        statement = (
            select(Psicologo)
            .join(PsicologoEspecialidad)
            .where(
                PsicologoEspecialidad.id_especialidad == especialidad_id,
                PsicologoEspecialidad.vigente == True,
                Psicologo.estado == 'activo'
            )
        )
    else:
        # Retornar todos los psicólogos activos
        statement = select(Psicologo).where(Psicologo.estado == 'activo')

    psicologos = session.exec(statement).all()

    return psicologos


from pydantic import BaseModel

class HorarioDisponibilidadInfo(BaseModel):
    """Información de disponibilidad de un horario"""
    hora: str
    disponible: bool
    ocupado: bool  # Si ya tiene una cita programada
    pasado: bool  # Si el horario ya pasó (solo para el día actual)

@router.get("/disponibilidad", response_model=list[HorarioDisponibilidadInfo])
def get_disponibilidad(
    session: SessionDep,
    psicologo_id: int = Query(..., description="ID del psicólogo"),
    fecha: date = Query(..., description="Fecha en formato YYYY-MM-DD")
) -> Any:
    """
    GET /api/disponibilidad?psicologo_id={id}&fecha={YYYY-MM-DD}

    Calcula y retorna horarios con su estado de disponibilidad.

    Lógica:
    1. Consultar tabla horarios_disponibles del psicólogo para ese día de semana
    2. Generar array de horarios posibles (intervalos de 1 hora)
    3. Consultar tabla citas para ver horarios ya ocupados en esa fecha
    4. Marcar horarios como ocupados, pasados o disponibles

    Respuesta: array de objetos con {hora, disponible, ocupado, pasado}
    """
    logger.info(f"===== INICIO get_disponibilidad psicologo_id={psicologo_id}, fecha={fecha} =====")

    # Verificar que el psicólogo existe
    psicologo = session.get(Psicologo, psicologo_id)
    if not psicologo:
        raise HTTPException(status_code=404, detail="Psicólogo no encontrado")

    # Obtener el día de la semana (en minúsculas, sin tildes, como en BD)
    dias_semana = {
        0: "lunes",
        1: "martes",
        2: "miercoles",
        3: "jueves",
        4: "viernes",
        5: "sabado",
        6: "domingo"
    }
    dia_semana = dias_semana[fecha.weekday()]
    logger.info(f"Día de la semana: {dia_semana}")

    # 1. Consultar horarios disponibles del psicólogo para ese día
    statement = select(HorarioDisponible).where(
        HorarioDisponible.id_psicologo == psicologo_id,
        HorarioDisponible.dia_semana == dia_semana,
        HorarioDisponible.disponible == True
    )
    horarios_config = session.exec(statement).all()
    logger.info(f"Horarios encontrados en BD: {len(horarios_config)}")

    if not horarios_config:
        logger.warning(f"NO HAY HORARIOS para psicologo {psicologo_id} en {dia_semana}")
        return []  # No hay horarios configurados para este día

    logger.info(f"Generando horarios para {len(horarios_config)} configuraciones")

    # 2. Generar array de horarios posibles (intervalos de 1 hora)
    horarios_disponibles = []
    for config in horarios_config:
        # Validar si el horario está dentro del rango de fechas (si está configurado)
        if config.fecha_desde and fecha < config.fecha_desde:
            continue
        if config.fecha_hasta and fecha > config.fecha_hasta:
            continue

        # Generar horarios desde hora_inicio hasta hora_fin
        hora_actual = datetime.combine(fecha, config.hora_inicio)
        hora_fin = datetime.combine(fecha, config.hora_fin)

        while hora_actual < hora_fin:
            horarios_disponibles.append(hora_actual.time())
            hora_actual += timedelta(hours=1)

    # 3. Consultar citas ya ocupadas en esa fecha
    statement = select(Cita).where(
        Cita.id_psicologo == psicologo_id,
        Cita.fecha_cita == fecha,
        Cita.id_estado_cita.in_([1, 2, 3])  # Pendiente, Confirmada, Realizada
    )
    citas_ocupadas = session.exec(statement).all()

    # 4. Identificar horarios ocupados
    horarios_ocupados = set()
    for cita in citas_ocupadas:
        # Marcar como ocupados todos los horarios entre hora_inicio y hora_fin
        hora_actual = datetime.combine(fecha, cita.hora_inicio)
        hora_fin_cita = datetime.combine(fecha, cita.hora_fin)

        while hora_actual < hora_fin_cita:
            horarios_ocupados.add(hora_actual.time())
            hora_actual += timedelta(hours=1)

    # 5. Determinar fecha y hora actual en Chile
    # Usar zoneinfo (disponible en Python 3.9+) para manejar correctamente la zona horaria
    from zoneinfo import ZoneInfo

    chile_tz = ZoneInfo('America/Santiago')
    now_chile = datetime.now(chile_tz)
    fecha_actual_chile = now_chile.date()
    hora_actual_chile = now_chile.time()

    es_hoy = (fecha == fecha_actual_chile)
    logger.info(f"Es hoy: {es_hoy}, Fecha consulta: {fecha}, Fecha actual Chile: {fecha_actual_chile}")
    if es_hoy:
        logger.info(f"Hora actual Chile: {hora_actual_chile}")

    # 6. Generar array con información completa de disponibilidad
    horarios_info = []
    for hora in sorted(set(horarios_disponibles)):
        es_ocupado = hora in horarios_ocupados
        # Un horario está pasado si es hoy Y la hora del slot ya pasó
        es_pasado = es_hoy and hora < hora_actual_chile
        es_disponible = not es_ocupado and not es_pasado

        horarios_info.append(HorarioDisponibilidadInfo(
            hora=hora.strftime("%H:%M"),
            disponible=es_disponible,
            ocupado=es_ocupado,
            pasado=es_pasado
        ))

    logger.info(f"Retornando {len(horarios_info)} horarios con su estado")
    return horarios_info
