"""
Servicio de envío de emails
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional

from sqlmodel import Session, select

from app.core.config import settings
from app.models import Notificacion, Cita
from app.email_templates import (
    get_confirmacion_inicial_template,
    get_confirmacion_final_template,
    get_cancelacion_template,
    get_reagendamiento_template,
    get_recordatorio_template
)


class EmailService:
    """Servicio para envío de emails"""

    @staticmethod
    def _send_email(
        destinatario: str,
        asunto: str,
        contenido_html: str
    ) -> tuple[bool, Optional[str]]:
        """
        Envía un email usando SMTP

        Returns:
            tuple: (success: bool, error_message: Optional[str])
        """
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = asunto
            msg['From'] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
            msg['To'] = destinatario

            # Adjuntar contenido HTML
            html_part = MIMEText(contenido_html, 'html', 'utf-8')
            msg.attach(html_part)

            # Conectar al servidor SMTP
            if settings.SMTP_TLS:
                server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
                server.starttls()
            else:
                server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)

            # Autenticación si hay credenciales
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

            # Enviar email
            server.send_message(msg)
            server.quit()

            return True, None

        except Exception as e:
            error_msg = f"Error al enviar email: {str(e)}"
            print(error_msg)  # Log para debug
            return False, error_msg

    @staticmethod
    def crear_notificacion_confirmacion_inicial(
        session: Session,
        cita: Cita,
        nombre_paciente: str,
        nombre_psicologo: str,
        nombre_servicio: str
    ) -> Notificacion:
        """Crea notificación de confirmación inicial (pendiente)"""

        # Formatear fecha
        fecha_formateada = cita.fecha_cita.strftime("%d/%m/%Y")
        hora_formateada = cita.hora_inicio.strftime("%H:%M")

        # Generar contenido HTML
        contenido = get_confirmacion_inicial_template(
            nombre_paciente=nombre_paciente,
            codigo_confirmacion=cita.codigo_confirmacion,
            fecha=fecha_formateada,
            hora_inicio=hora_formateada,
            nombre_psicologo=nombre_psicologo,
            nombre_servicio=nombre_servicio
        )

        # Obtener email del paciente
        email_paciente = cita.paciente.email

        # Crear notificación
        notificacion = Notificacion(
            id_cita=cita.id_cita,
            email_destinatario=email_paciente,
            tipo_notificacion="confirmacion_inicial",
            asunto=f"Solicitud de cita recibida - Código: {cita.codigo_confirmacion}",
            contenido=contenido,
            estado="pendiente"
        )

        session.add(notificacion)
        session.commit()
        session.refresh(notificacion)

        return notificacion

    @staticmethod
    def crear_notificacion_confirmacion_final(
        session: Session,
        cita: Cita,
        nombre_paciente: str,
        nombre_psicologo: str,
        nombre_servicio: str
    ) -> Notificacion:
        """Crea notificación de confirmación final (confirmada)"""
        from datetime import datetime as dt, timedelta
        from app.email_templates import generate_calendar_links

        # Formatear fecha
        fecha_formateada = cita.fecha_cita.strftime("%d/%m/%Y")
        hora_formateada = cita.hora_inicio.strftime("%H:%M")

        # Generar enlaces de calendario
        fecha_hora_inicio = dt.combine(cita.fecha_cita, cita.hora_inicio)
        fecha_hora_fin = dt.combine(cita.fecha_cita, cita.hora_fin)

        titulo = f"Cita - {nombre_servicio} con {nombre_psicologo}"
        descripcion = f"Cita de {nombre_servicio} con {nombre_psicologo}\nPaciente: {nombre_paciente}"
        ubicacion = "Conectemos Chile"

        calendar_links = generate_calendar_links(
            titulo=titulo,
            descripcion=descripcion,
            fecha_hora_inicio=fecha_hora_inicio.isoformat(),
            fecha_hora_fin=fecha_hora_fin.isoformat(),
            ubicacion=ubicacion
        )

        # Generar contenido HTML
        contenido = get_confirmacion_final_template(
            nombre_paciente=nombre_paciente,
            fecha=fecha_formateada,
            hora_inicio=hora_formateada,
            nombre_psicologo=nombre_psicologo,
            nombre_servicio=nombre_servicio,
            google_calendar_url=calendar_links["google"],
            outlook_calendar_url=calendar_links["outlook"]
        )

        # Obtener email del paciente
        email_paciente = cita.paciente.email

        # Crear notificación
        notificacion = Notificacion(
            id_cita=cita.id_cita,
            email_destinatario=email_paciente,
            tipo_notificacion="confirmacion_final",
            asunto=f"✅ Cita confirmada - {fecha_formateada} a las {hora_formateada}",
            contenido=contenido,
            estado="pendiente"
        )

        session.add(notificacion)
        session.commit()
        session.refresh(notificacion)

        return notificacion

    @staticmethod
    def crear_notificacion_cancelacion(
        session: Session,
        cita: Cita,
        nombre_paciente: str,
        nombre_psicologo: str
    ) -> Notificacion:
        """Crea notificación de cancelación"""

        # Formatear fecha
        fecha_formateada = cita.fecha_cita.strftime("%d/%m/%Y")
        hora_formateada = cita.hora_inicio.strftime("%H:%M")

        # Generar contenido HTML
        contenido = get_cancelacion_template(
            nombre_paciente=nombre_paciente,
            fecha=fecha_formateada,
            hora_inicio=hora_formateada,
            nombre_psicologo=nombre_psicologo
        )

        # Obtener email del paciente
        email_paciente = cita.paciente.email

        # Crear notificación
        notificacion = Notificacion(
            id_cita=cita.id_cita,
            email_destinatario=email_paciente,
            tipo_notificacion="cancelacion",
            asunto=f"Cita cancelada - {fecha_formateada}",
            contenido=contenido,
            estado="pendiente"
        )

        session.add(notificacion)
        session.commit()
        session.refresh(notificacion)

        return notificacion

    @staticmethod
    def crear_notificacion_reagendamiento(
        session: Session,
        cita: Cita,
        nombre_paciente: str,
        nombre_psicologo: str,
        nombre_servicio: str,
        fecha_antigua: datetime,
        hora_antigua: datetime
    ) -> Notificacion:
        """Crea notificación de reagendamiento"""

        # Formatear fechas
        fecha_antigua_fmt = fecha_antigua.strftime("%d/%m/%Y")
        hora_antigua_fmt = hora_antigua.strftime("%H:%M")
        fecha_nueva_fmt = cita.fecha_cita.strftime("%d/%m/%Y")
        hora_nueva_fmt = cita.hora_inicio.strftime("%H:%M")

        # Generar contenido HTML
        contenido = get_reagendamiento_template(
            nombre_paciente=nombre_paciente,
            fecha_antigua=fecha_antigua_fmt,
            hora_antigua=hora_antigua_fmt,
            fecha_nueva=fecha_nueva_fmt,
            hora_nueva=hora_nueva_fmt,
            nombre_psicologo=nombre_psicologo,
            nombre_servicio=nombre_servicio
        )

        # Obtener email del paciente
        email_paciente = cita.paciente.email

        # Crear notificación
        notificacion = Notificacion(
            id_cita=cita.id_cita,
            email_destinatario=email_paciente,
            tipo_notificacion="reagendamiento",
            asunto=f"🔄 Cita reagendada - Nueva fecha: {fecha_nueva_fmt}",
            contenido=contenido,
            estado="pendiente"
        )

        session.add(notificacion)
        session.commit()
        session.refresh(notificacion)

        return notificacion

    @staticmethod
    def enviar_notificacion(
        session: Session,
        notificacion_id: int
    ) -> bool:
        """
        Envía una notificación pendiente

        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        # Obtener notificación
        notificacion = session.get(Notificacion, notificacion_id)

        if not notificacion:
            return False

        # Incrementar intentos
        notificacion.intentos_envio += 1

        # Enviar email
        success, error_msg = EmailService._send_email(
            destinatario=notificacion.email_destinatario,
            asunto=notificacion.asunto,
            contenido_html=notificacion.contenido
        )

        # Actualizar estado
        if success:
            notificacion.estado = "enviada"
            notificacion.fecha_enviada = datetime.utcnow()
            notificacion.error_mensaje = None
        else:
            # Si falló 3 veces, marcar como fallida
            if notificacion.intentos_envio >= 3:
                notificacion.estado = "fallida"
            notificacion.error_mensaje = error_msg

        session.add(notificacion)
        session.commit()

        return success

    @staticmethod
    def enviar_notificaciones_pendientes(session: Session) -> dict:
        """
        Procesa y envía todas las notificaciones pendientes

        Returns:
            dict: Estadísticas de envío {enviadas, fallidas, pendientes}
        """
        # Obtener notificaciones pendientes
        statement = select(Notificacion).where(
            Notificacion.estado == "pendiente",
            Notificacion.intentos_envio < 3
        )
        notificaciones = session.exec(statement).all()

        enviadas = 0
        fallidas = 0

        for notif in notificaciones:
            success = EmailService.enviar_notificacion(session, notif.id_notificacion)
            if success:
                enviadas += 1
            else:
                fallidas += 1

        return {
            "enviadas": enviadas,
            "fallidas": fallidas,
            "total_procesadas": len(notificaciones)
        }
