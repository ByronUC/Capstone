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


@router.get("/disponibilidad", response_model=list[str])
def get_disponibilidad(
    session: SessionDep,
    psicologo_id: int = Query(..., description="ID del psicólogo"),
    fecha: date = Query(..., description="Fecha en formato YYYY-MM-DD")
) -> Any:
    """
    GET /api/disponibilidad?psicologo_id={id}&fecha={YYYY-MM-DD}

    Calcula y retorna horarios disponibles para ese psicólogo en esa fecha.

    Lógica:
    1. Consultar tabla horarios_disponibles del psicólogo para ese día de semana
    2. Generar array de horarios posibles (intervalos de 1 hora)
    3. Consultar tabla citas para ver horarios ya ocupados en esa fecha
    4. Restar ocupados de disponibles

    Respuesta: array de strings con horarios ["09:00", "10:00", "11:00"]
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

    # 4. Restar horarios ocupados
    horarios_ocupados = set()
    for cita in citas_ocupadas:
        # Marcar como ocupados todos los horarios entre hora_inicio y hora_fin
        hora_actual = datetime.combine(fecha, cita.hora_inicio)
        hora_fin_cita = datetime.combine(fecha, cita.hora_fin)

        while hora_actual < hora_fin_cita:
            horarios_ocupados.add(hora_actual.time())
            hora_actual += timedelta(hours=1)

    # Filtrar horarios disponibles quitando los ocupados
    horarios_libres = [
        h for h in horarios_disponibles
        if h not in horarios_ocupados
    ]

    # Convertir a formato string HH:MM
    horarios_libres_str = [h.strftime("%H:%M") for h in sorted(set(horarios_libres))]

    logger.info(f"Retornando {len(horarios_libres_str)} horarios disponibles")
    return horarios_libres_str
