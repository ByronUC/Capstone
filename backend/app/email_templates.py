"""
Templates HTML para emails del sistema de citas
"""
from datetime import datetime
from urllib.parse import quote


def generate_calendar_links(titulo: str, descripcion: str, fecha_hora_inicio: str, fecha_hora_fin: str, ubicacion: str = "") -> dict:
    """
    Genera enlaces para agregar evento a diferentes calendarios

    Args:
        titulo: Título del evento
        descripcion: Descripción del evento
        fecha_hora_inicio: Fecha y hora de inicio en formato ISO (YYYY-MM-DDTHH:MM:SS)
        fecha_hora_fin: Fecha y hora de fin en formato ISO (YYYY-MM-DDTHH:MM:SS)
        ubicacion: Ubicación del evento (opcional)

    Returns:
        dict con enlaces para Google Calendar, Outlook, etc.
    """
    # Convertir formato ISO a formato para Google Calendar (YYYYMMDDTHHMMSS)
    inicio_dt = datetime.fromisoformat(fecha_hora_inicio)
    fin_dt = datetime.fromisoformat(fecha_hora_fin)

    inicio_google = inicio_dt.strftime("%Y%m%dT%H%M%S")
    fin_google = fin_dt.strftime("%Y%m%dT%H%M%S")

    # Google Calendar
    google_url = (
        f"https://www.google.com/calendar/render?action=TEMPLATE"
        f"&text={quote(titulo)}"
        f"&dates={inicio_google}/{fin_google}"
        f"&details={quote(descripcion)}"
        f"&location={quote(ubicacion)}"
    )

    # Outlook/Office 365
    outlook_url = (
        f"https://outlook.office.com/calendar/0/deeplink/compose?"
        f"subject={quote(titulo)}"
        f"&body={quote(descripcion)}"
        f"&startdt={fecha_hora_inicio}"
        f"&enddt={fecha_hora_fin}"
        f"&location={quote(ubicacion)}"
    )

    # iCal/Apple Calendar (archivo .ics)
    # Este se generaría en el backend y se enviaría como adjunto

    return {
        "google": google_url,
        "outlook": outlook_url
    }


def get_confirmacion_inicial_template(
    nombre_paciente: str,
    codigo_confirmacion: str,
    fecha: str,
    hora_inicio: str,
    nombre_psicologo: str,
    nombre_servicio: str
) -> str:
    """Template para confirmación inicial (estado: Pendiente)"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #3182CE; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background-color: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
            .info-box {{ background-color: white; padding: 20px; margin: 20px 0; border-left: 4px solid #3182CE; border-radius: 4px; }}
            .codigo {{ font-size: 24px; font-weight: bold; color: #3182CE; letter-spacing: 2px; text-align: center; padding: 15px; background-color: #EBF8FF; border-radius: 4px; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            .button {{ display: inline-block; padding: 12px 30px; background-color: #3182CE; color: white; text-decoration: none; border-radius: 4px; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Solicitud de Cita Recibida</h1>
            </div>
            <div class="content">
                <h2>Hola {nombre_paciente},</h2>
                <p>Hemos recibido tu solicitud de cita. Tu reserva está <strong>pendiente de confirmación</strong> por nuestro equipo de recepción.</p>

                <div class="codigo">
                    {codigo_confirmacion}
                </div>
                <p style="text-align: center; margin-top: -10px; color: #666;">
                    <small>Guarda este código para gestionar tu cita</small>
                </p>

                <div class="info-box">
                    <p><strong>📅 Fecha:</strong> {fecha}</p>
                    <p><strong>🕐 Hora:</strong> {hora_inicio}</p>
                    <p><strong>👨‍⚕️ Psicólogo(a):</strong> {nombre_psicologo}</p>
                    <p><strong>🏥 Servicio:</strong> {nombre_servicio}</p>
                    <p><strong>📋 Estado:</strong> <span style="color: #D69E2E;">Pendiente de confirmación</span></p>
                </div>

                <p><strong>Próximos pasos:</strong></p>
                <ul>
                    <li>Nuestro equipo revisará tu solicitud</li>
                    <li>Recibirás un email de confirmación dentro de las próximas 24 horas</li>
                    <li>Si tienes dudas, contáctanos respondiendo este email</li>
                </ul>

                <p>Puedes reagendar o cancelar tu cita usando tu código de confirmación en:</p>
                <div style="text-align: center;">
                    <a href="http://localhost:5173/gestionar-cita" class="button">Gestionar mi Cita</a>
                </div>
            </div>
            <div class="footer">
                <p>Conectemos Chile - Salud Mental<br>
                contacto@conectemoschile.cl<br>
                Este es un email automático, por favor no respondas directamente.</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_confirmacion_final_template(
    nombre_paciente: str,
    fecha: str,
    hora_inicio: str,
    nombre_psicologo: str,
    nombre_servicio: str,
    google_calendar_url: str = "",
    outlook_calendar_url: str = "",
    direccion: str = "Av. Providencia 1234, Santiago"
) -> str:
    """Template para confirmación final (estado: Confirmada)"""

    # Botones de calendario
    calendar_buttons = ""
    if google_calendar_url or outlook_calendar_url:
        calendar_buttons = '<div style="text-align: center; margin: 30px 0;">'
        calendar_buttons += '<p style="margin-bottom: 15px;"><strong>📅 Agregar a tu calendario:</strong></p>'

        if google_calendar_url:
            calendar_buttons += f'''
            <a href="{google_calendar_url}" target="_blank"
               style="display: inline-block; padding: 12px 24px; margin: 5px; background-color: #4285F4;
                      color: white; text-decoration: none; border-radius: 4px; font-weight: bold;">
                📅 Google Calendar
            </a>
            '''

        if outlook_calendar_url:
            calendar_buttons += f'''
            <a href="{outlook_calendar_url}" target="_blank"
               style="display: inline-block; padding: 12px 24px; margin: 5px; background-color: #0078D4;
                      color: white; text-decoration: none; border-radius: 4px; font-weight: bold;">
                📅 Outlook
            </a>
            '''

        calendar_buttons += '</div>'

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #38A169; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background-color: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
            .info-box {{ background-color: white; padding: 20px; margin: 20px 0; border-left: 4px solid #38A169; border-radius: 4px; }}
            .success {{ background-color: #C6F6D5; color: #22543D; padding: 15px; border-radius: 4px; text-align: center; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>✅ Cita Confirmada</h1>
            </div>
            <div class="content">
                <h2>Hola {nombre_paciente},</h2>

                <div class="success">
                    <strong>¡Tu cita ha sido confirmada exitosamente!</strong>
                </div>

                <p>Tu cita está agendada y confirmada. Por favor, ten en cuenta los siguientes detalles:</p>

                <div class="info-box">
                    <p><strong>📅 Fecha:</strong> {fecha}</p>
                    <p><strong>🕐 Hora:</strong> {hora_inicio}</p>
                    <p><strong>👨‍⚕️ Psicólogo(a):</strong> {nombre_psicologo}</p>
                    <p><strong>🏥 Servicio:</strong> {nombre_servicio}</p>
                    <p><strong>📍 Dirección:</strong> {direccion}</p>
                </div>

                {calendar_buttons}

                <p><strong>Recomendaciones:</strong></p>
                <ul>
                    <li>Llega 10 minutos antes de tu cita</li>
                    <li>Trae tu documento de identidad</li>
                    <li>Si no puedes asistir, avísanos con al menos 24 horas de anticipación</li>
                </ul>

                <p>Esperamos verte pronto. Si tienes alguna pregunta, no dudes en contactarnos.</p>
            </div>
            <div class="footer">
                <p>Conectemos Chile - Salud Mental<br>
                contacto@conectemoschile.cl | Tel: +56 2 1234 5678<br>
                {direccion}</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_cancelacion_template(
    nombre_paciente: str,
    fecha: str,
    hora_inicio: str,
    nombre_psicologo: str
) -> str:
    """Template para cancelación de cita"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #E53E3E; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background-color: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
            .info-box {{ background-color: white; padding: 20px; margin: 20px 0; border-left: 4px solid #E53E3E; border-radius: 4px; }}
            .button {{ display: inline-block; padding: 12px 30px; background-color: #3182CE; color: white; text-decoration: none; border-radius: 4px; margin: 10px 0; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Cita Cancelada</h1>
            </div>
            <div class="content">
                <h2>Hola {nombre_paciente},</h2>
                <p>Tu cita ha sido cancelada correctamente.</p>

                <div class="info-box">
                    <p><strong>📅 Fecha cancelada:</strong> {fecha}</p>
                    <p><strong>🕐 Hora:</strong> {hora_inicio}</p>
                    <p><strong>👨‍⚕️ Psicólogo(a):</strong> {nombre_psicologo}</p>
                </div>

                <p>Esperamos poder atenderte en otra ocasión. Si deseas agendar una nueva cita, puedes hacerlo en cualquier momento:</p>

                <div style="text-align: center;">
                    <a href="http://localhost:5173/#booking" class="button">Reservar Nueva Cita</a>
                </div>

                <p>Si la cancelación fue un error o tienes alguna pregunta, contáctanos.</p>
            </div>
            <div class="footer">
                <p>Conectemos Chile - Salud Mental<br>
                contacto@conectemoschile.cl</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_reagendamiento_template(
    nombre_paciente: str,
    fecha_antigua: str,
    hora_antigua: str,
    fecha_nueva: str,
    hora_nueva: str,
    nombre_psicologo: str,
    nombre_servicio: str
) -> str:
    """Template para reagendamiento de cita"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #D69E2E; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background-color: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
            .info-box {{ background-color: white; padding: 20px; margin: 20px 0; border-radius: 4px; }}
            .old-date {{ text-decoration: line-through; color: #999; }}
            .new-date {{ color: #D69E2E; font-weight: bold; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔄 Cita Reagendada</h1>
            </div>
            <div class="content">
                <h2>Hola {nombre_paciente},</h2>
                <p>Tu cita ha sido reagendada correctamente.</p>

                <div class="info-box" style="border-left: 4px solid #FC8181;">
                    <h3 style="margin-top: 0;">Fecha anterior (cancelada):</h3>
                    <p class="old-date">📅 {fecha_antigua} a las {hora_antigua}</p>
                </div>

                <div class="info-box" style="border-left: 4px solid #38A169;">
                    <h3 style="margin-top: 0;">Nueva fecha confirmada:</h3>
                    <p class="new-date">📅 {fecha_nueva} a las {hora_nueva}</p>
                    <p><strong>👨‍⚕️ Psicólogo(a):</strong> {nombre_psicologo}</p>
                    <p><strong>🏥 Servicio:</strong> {nombre_servicio}</p>
                </div>

                <p><strong>Recordatorio:</strong></p>
                <ul>
                    <li>Llega 10 minutos antes de tu cita</li>
                    <li>Trae tu documento de identidad</li>
                    <li>Si necesitas cancelar o volver a reagendar, hazlo con al menos 24 horas de anticipación</li>
                </ul>

                <p>Nos vemos en la nueva fecha. ¡Gracias por tu comprensión!</p>
            </div>
            <div class="footer">
                <p>Conectemos Chile - Salud Mental<br>
                contacto@conectemoschile.cl</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_recordatorio_template(
    nombre_paciente: str,
    fecha: str,
    hora_inicio: str,
    nombre_psicologo: str,
    direccion: str = "Av. Providencia 1234, Santiago"
) -> str:
    """Template para recordatorio 24h antes"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #805AD5; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background-color: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
            .info-box {{ background-color: white; padding: 20px; margin: 20px 0; border-left: 4px solid #805AD5; border-radius: 4px; }}
            .reminder {{ background-color: #FAF089; padding: 15px; border-radius: 4px; text-align: center; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>⏰ Recordatorio de Cita</h1>
            </div>
            <div class="content">
                <h2>Hola {nombre_paciente},</h2>

                <div class="reminder">
                    <strong>🔔 ¡Tu cita es mañana!</strong>
                </div>

                <p>Te recordamos que tienes una cita agendada para mañana:</p>

                <div class="info-box">
                    <p><strong>📅 Fecha:</strong> {fecha}</p>
                    <p><strong>🕐 Hora:</strong> {hora_inicio}</p>
                    <p><strong>👨‍⚕️ Psicólogo(a):</strong> {nombre_psicologo}</p>
                    <p><strong>📍 Dirección:</strong> {direccion}</p>
                </div>

                <p><strong>Recomendaciones:</strong></p>
                <ul>
                    <li>✅ Llega 10 minutos antes</li>
                    <li>✅ Trae tu documento de identidad</li>
                    <li>✅ Si tienes documentos o exámenes previos, tráelos contigo</li>
                </ul>

                <p>Si no puedes asistir, por favor cancela tu cita lo antes posible para que podamos ofrecerla a otro paciente.</p>

                <p>¡Te esperamos!</p>
            </div>
            <div class="footer">
                <p>Conectemos Chile - Salud Mental<br>
                contacto@conectemoschile.cl | Tel: +56 2 1234 5678<br>
                {direccion}</p>
            </div>
        </div>
    </body>
    </html>
    """


# ========== TEMPLATES PARA PSICÓLOGOS ==========

def get_confirmacion_inicial_psicologo_template(
    nombre_psicologo: str,
    nombre_paciente: str,
    fecha: str,
    hora_inicio: str,
    hora_fin: str,
    nombre_servicio: str,
    telefono_paciente: str = ""
) -> str:
    """Template para notificar al psicólogo sobre nueva solicitud de cita pendiente"""
    telefono_info = ""
    if telefono_paciente:
        telefono_info = f"<p><strong>📞 Teléfono:</strong> {telefono_paciente}</p>"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #3182CE; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background-color: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
            .info-box {{ background-color: white; padding: 20px; margin: 20px 0; border-left: 4px solid #3182CE; border-radius: 4px; }}
            .status {{ font-size: 18px; font-weight: bold; color: #D69E2E; text-align: center; padding: 15px; background-color: #FEEBC8; border-radius: 4px; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Nueva Solicitud de Cita</h1>
            </div>
            <div class="content">
                <h2>Hola {nombre_psicologo},</h2>

                <div class="status">
                    ⏳ Solicitud Pendiente de Confirmación
                </div>

                <p>Se ha recibido una nueva solicitud de cita que requiere tu atención:</p>

                <div class="info-box">
                    <p><strong>👤 Paciente:</strong> {nombre_paciente}</p>
                    {telefono_info}
                    <p><strong>📅 Fecha:</strong> {fecha}</p>
                    <p><strong>🕐 Horario:</strong> {hora_inicio} - {hora_fin}</p>
                    <p><strong>🏥 Servicio:</strong> {nombre_servicio}</p>
                </div>

                <p><strong>Próximos pasos:</strong></p>
                <ul>
                    <li>El equipo de recepción revisará y confirmará la disponibilidad</li>
                    <li>Una vez confirmada, recibirás un email de confirmación final</li>
                    <li>La cita aparecerá en tu agenda del sistema</li>
                </ul>

                <p>Este es un email informativo. No necesitas tomar ninguna acción en este momento.</p>
            </div>
            <div class="footer">
                <p>Conectemos Chile - Sistema de Gestión de Citas<br>
                Este es un email automático del sistema.</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_confirmacion_final_psicologo_template(
    nombre_psicologo: str,
    nombre_paciente: str,
    fecha: str,
    hora_inicio: str,
    hora_fin: str,
    nombre_servicio: str,
    telefono_paciente: str = "",
    google_calendar_url: str = "",
    outlook_calendar_url: str = ""
) -> str:
    """Template para notificar al psicólogo sobre cita confirmada"""
    telefono_info = ""
    if telefono_paciente:
        telefono_info = f"<p><strong>📞 Teléfono:</strong> {telefono_paciente}</p>"

    # Botones de calendario
    calendar_buttons = ""
    if google_calendar_url or outlook_calendar_url:
        calendar_buttons = '<div style="text-align: center; margin: 30px 0;">'
        calendar_buttons += '<p style="margin-bottom: 15px;"><strong>📅 Agregar a tu calendario:</strong></p>'

        if google_calendar_url:
            calendar_buttons += f'''
            <a href="{google_calendar_url}" target="_blank"
               style="display: inline-block; padding: 12px 24px; margin: 5px; background-color: #4285F4;
                      color: white; text-decoration: none; border-radius: 4px; font-weight: bold;">
                📅 Google Calendar
            </a>
            '''

        if outlook_calendar_url:
            calendar_buttons += f'''
            <a href="{outlook_calendar_url}" target="_blank"
               style="display: inline-block; padding: 12px 24px; margin: 5px; background-color: #0078D4;
                      color: white; text-decoration: none; border-radius: 4px; font-weight: bold;">
                📅 Outlook
            </a>
            '''

        calendar_buttons += '</div>'

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #38A169; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background-color: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
            .info-box {{ background-color: white; padding: 20px; margin: 20px 0; border-left: 4px solid #38A169; border-radius: 4px; }}
            .success {{ background-color: #C6F6D5; color: #22543D; padding: 15px; border-radius: 4px; text-align: center; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>✅ Cita Confirmada en tu Agenda</h1>
            </div>
            <div class="content">
                <h2>Hola {nombre_psicologo},</h2>

                <div class="success">
                    <strong>Nueva cita confirmada y agregada a tu agenda</strong>
                </div>

                <p>Se ha confirmado una nueva cita en tu agenda profesional:</p>

                <div class="info-box">
                    <p><strong>👤 Paciente:</strong> {nombre_paciente}</p>
                    {telefono_info}
                    <p><strong>📅 Fecha:</strong> {fecha}</p>
                    <p><strong>🕐 Horario:</strong> {hora_inicio} - {hora_fin}</p>
                    <p><strong>🏥 Servicio:</strong> {nombre_servicio}</p>
                </div>

                {calendar_buttons}

                <p><strong>Recordatorio:</strong></p>
                <ul>
                    <li>El paciente ha sido notificado y recibirá un recordatorio 24 horas antes</li>
                    <li>Puedes ver todos los detalles de la cita en el sistema de gestión</li>
                    <li>Si necesitas cancelar o reagendar, coordina con recepción</li>
                </ul>

                <p>¡Éxito en tu sesión!</p>
            </div>
            <div class="footer">
                <p>Conectemos Chile - Sistema de Gestión de Citas<br>
                Este es un email automático del sistema.</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_cancelacion_psicologo_template(
    nombre_psicologo: str,
    nombre_paciente: str,
    fecha: str,
    hora_inicio: str,
    hora_fin: str,
    nombre_servicio: str
) -> str:
    """Template para notificar al psicólogo sobre cancelación de cita"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #E53E3E; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background-color: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
            .info-box {{ background-color: white; padding: 20px; margin: 20px 0; border-left: 4px solid #E53E3E; border-radius: 4px; }}
            .alert {{ background-color: #FED7D7; color: #742A2A; padding: 15px; border-radius: 4px; text-align: center; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>❌ Cita Cancelada</h1>
            </div>
            <div class="content">
                <h2>Hola {nombre_psicologo},</h2>

                <div class="alert">
                    <strong>Una cita ha sido cancelada</strong>
                </div>

                <p>Te informamos que la siguiente cita ha sido cancelada:</p>

                <div class="info-box">
                    <p><strong>👤 Paciente:</strong> {nombre_paciente}</p>
                    <p><strong>📅 Fecha:</strong> {fecha}</p>
                    <p><strong>🕐 Horario:</strong> {hora_inicio} - {hora_fin}</p>
                    <p><strong>🏥 Servicio:</strong> {nombre_servicio}</p>
                </div>

                <p>El horario ahora está disponible en tu agenda para nuevas reservas.</p>

                <p>Si tienes alguna pregunta sobre esta cancelación, contacta con recepción.</p>
            </div>
            <div class="footer">
                <p>Conectemos Chile - Sistema de Gestión de Citas<br>
                Este es un email automático del sistema.</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_reagendamiento_psicologo_template(
    nombre_psicologo: str,
    nombre_paciente: str,
    fecha_antigua: str,
    hora_antigua_inicio: str,
    hora_antigua_fin: str,
    fecha_nueva: str,
    hora_nueva_inicio: str,
    hora_nueva_fin: str,
    nombre_servicio: str
) -> str:
    """Template para notificar al psicólogo sobre reagendamiento de cita"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #D69E2E; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background-color: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
            .info-box {{ background-color: white; padding: 20px; margin: 20px 0; border-radius: 4px; }}
            .old-date {{ text-decoration: line-through; color: #999; }}
            .new-date {{ color: #D69E2E; font-weight: bold; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔄 Cita Reagendada</h1>
            </div>
            <div class="content">
                <h2>Hola {nombre_psicologo},</h2>

                <p>Te informamos que una cita ha sido reagendada en tu agenda:</p>

                <p><strong>👤 Paciente:</strong> {nombre_paciente}</p>
                <p><strong>🏥 Servicio:</strong> {nombre_servicio}</p>

                <div class="info-box" style="border-left: 4px solid #FC8181;">
                    <h3 style="margin-top: 0;">Fecha anterior (cancelada):</h3>
                    <p class="old-date">📅 {fecha_antigua}</p>
                    <p class="old-date">🕐 {hora_antigua_inicio} - {hora_antigua_fin}</p>
                </div>

                <div class="info-box" style="border-left: 4px solid #38A169;">
                    <h3 style="margin-top: 0;">Nueva fecha confirmada:</h3>
                    <p class="new-date">📅 {fecha_nueva}</p>
                    <p class="new-date">🕐 {hora_nueva_inicio} - {hora_nueva_fin}</p>
                </div>

                <p>La cita ha sido actualizada automáticamente en tu agenda del sistema.</p>

                <p>El paciente ha sido notificado del cambio y recibirá un recordatorio 24 horas antes de la nueva fecha.</p>
            </div>
            <div class="footer">
                <p>Conectemos Chile - Sistema de Gestión de Citas<br>
                Este es un email automático del sistema.</p>
            </div>
        </div>
    </body>
    </html>
    """
