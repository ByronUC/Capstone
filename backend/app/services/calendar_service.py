"""
Servicio de Google Calendar
"""
from datetime import datetime, timedelta
from typing import Optional
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class GoogleCalendarService:
    """Servicio para interactuar con Google Calendar API"""

    def __init__(self):
        self.enabled = settings.GOOGLE_CALENDAR_ENABLED
        self.calendar_id = settings.GOOGLE_CALENDAR_ID
        self.service = None

        if self.enabled:
            try:
                self._initialize_service()
            except Exception as e:
                logger.error(f"Error inicializando Google Calendar: {e}")
                self.enabled = False

    def _initialize_service(self):
        """Inicializa el servicio de Google Calendar"""
        if not self.enabled:
            return

        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build

            # Cargar credenciales
            credentials = service_account.Credentials.from_service_account_file(
                settings.GOOGLE_CALENDAR_CREDENTIALS_PATH,
                scopes=['https://www.googleapis.com/auth/calendar']
            )

            # Crear servicio
            self.service = build('calendar', 'v3', credentials=credentials)
            logger.info("Google Calendar service initialized successfully")

        except ImportError:
            logger.warning("Google Calendar libraries not installed. Run: pip install google-auth google-api-python-client")
            self.enabled = False
        except Exception as e:
            logger.error(f"Error creating Google Calendar service: {e}")
            self.enabled = False

    def create_event(
        self,
        titulo: str,
        descripcion: str,
        fecha_inicio: datetime,
        duracion_minutos: int,
        email_paciente: str,
        email_psicologo: Optional[str] = None
    ) -> Optional[str]:
        """
        Crea un evento en Google Calendar

        Args:
            titulo: Título del evento
            descripcion: Descripción del evento
            fecha_inicio: Fecha y hora de inicio
            duracion_minutos: Duración en minutos
            email_paciente: Email del paciente
            email_psicologo: Email del psicólogo (opcional)

        Returns:
            str: ID del evento creado, o None si falló
        """
        if not self.enabled or not self.service:
            logger.warning("Google Calendar not enabled")
            return None

        try:
            # Calcular fecha de fin
            fecha_fin = fecha_inicio + timedelta(minutes=duracion_minutos)

            # NOTA: No agregamos 'attendees' porque Service Accounts requieren
            # Domain-Wide Delegation para invitar asistentes. El evento solo
            # aparecerá en el calendario del Service Account compartido.
            # Los emails de notificación a pacientes se envían por separado.

            # Crear evento
            event = {
                'summary': titulo,
                'description': descripcion,
                'start': {
                    'dateTime': fecha_inicio.isoformat(),
                    'timeZone': 'America/Santiago',
                },
                'end': {
                    'dateTime': fecha_fin.isoformat(),
                    'timeZone': 'America/Santiago',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},  # 24 horas antes
                        {'method': 'popup', 'minutes': 60},       # 1 hora antes
                    ],
                },
            }

            # Insertar evento
            created_event = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event,
                sendUpdates='none'  # No enviar notificaciones (manejadas por email_service)
            ).execute()

            logger.info(f"Event created: {created_event.get('id')}")
            return created_event.get('id')

        except Exception as e:
            logger.error(f"Error creating calendar event: {e}")
            return None

    def update_event(
        self,
        event_id: str,
        titulo: str,
        descripcion: str,
        fecha_inicio: datetime,
        duracion_minutos: int,
        email_paciente: str,
        email_psicologo: Optional[str] = None
    ) -> bool:
        """
        Actualiza un evento existente en Google Calendar

        Args:
            event_id: ID del evento a actualizar
            titulo: Nuevo título del evento
            descripcion: Nueva descripción
            fecha_inicio: Nueva fecha y hora de inicio
            duracion_minutos: Nueva duración en minutos
            email_paciente: Email del paciente
            email_psicologo: Email del psicólogo (opcional)

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        if not self.enabled or not self.service:
            logger.warning("Google Calendar not enabled")
            return False

        try:
            # Calcular fecha de fin
            fecha_fin = fecha_inicio + timedelta(minutes=duracion_minutos)

            # Obtener evento existente
            event = self.service.events().get(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()

            # Actualizar campos
            event['summary'] = titulo
            event['description'] = descripcion
            event['start'] = {
                'dateTime': fecha_inicio.isoformat(),
                'timeZone': 'America/Santiago',
            }
            event['end'] = {
                'dateTime': fecha_fin.isoformat(),
                'timeZone': 'America/Santiago',
            }
            # No actualizamos 'attendees' (ver nota en create_event)

            # Actualizar evento
            updated_event = self.service.events().update(
                calendarId=self.calendar_id,
                eventId=event_id,
                body=event,
                sendUpdates='none'  # No enviar notificaciones (manejadas por email_service)
            ).execute()

            logger.info(f"Event updated: {updated_event.get('id')}")
            return True

        except Exception as e:
            logger.error(f"Error updating calendar event: {e}")
            return False

    def delete_event(self, event_id: str) -> bool:
        """
        Elimina un evento de Google Calendar

        Args:
            event_id: ID del evento a eliminar

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        if not self.enabled or not self.service:
            logger.warning("Google Calendar not enabled")
            return False

        try:
            self.service.events().delete(
                calendarId=self.calendar_id,
                eventId=event_id,
                sendUpdates='none'  # No enviar notificaciones (manejadas por email_service)
            ).execute()

            logger.info(f"Event deleted: {event_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting calendar event: {e}")
            return False


# Instancia singleton del servicio
calendar_service = GoogleCalendarService()
