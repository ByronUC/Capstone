-- Migración: Agregar soporte para notificaciones y Google Calendar
-- Fecha: 2025-10-30

-- 1. Agregar campo google_calendar_event_id a tabla citas
ALTER TABLE citas
ADD COLUMN IF NOT EXISTS google_calendar_event_id VARCHAR(255);

-- Crear índice para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_citas_google_event ON citas(google_calendar_event_id);

-- 2. Crear tabla de notificaciones
CREATE TABLE IF NOT EXISTS notificaciones (
    id_notificacion SERIAL PRIMARY KEY,
    id_cita INTEGER REFERENCES citas(id_cita) ON DELETE CASCADE,
    email_destinatario VARCHAR(255) NOT NULL,
    tipo_notificacion VARCHAR(50) NOT NULL, -- 'confirmacion_inicial', 'confirmacion_final', 'cancelacion', 'reagendamiento', 'recordatorio'
    asunto VARCHAR(255) NOT NULL,
    contenido TEXT NOT NULL,
    estado VARCHAR(20) DEFAULT 'pendiente', -- 'pendiente', 'enviada', 'fallida'
    intentos_envio INTEGER DEFAULT 0,
    fecha_programada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_enviada TIMESTAMP,
    error_mensaje TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para la tabla notificaciones
CREATE INDEX IF NOT EXISTS idx_notificaciones_estado ON notificaciones(estado);
CREATE INDEX IF NOT EXISTS idx_notificaciones_fecha_programada ON notificaciones(fecha_programada);
CREATE INDEX IF NOT EXISTS idx_notificaciones_cita ON notificaciones(id_cita);

-- Comentarios descriptivos
COMMENT ON TABLE notificaciones IS 'Registro de todas las notificaciones por email del sistema';
COMMENT ON COLUMN notificaciones.tipo_notificacion IS 'Tipo de notificación: confirmacion_inicial, confirmacion_final, cancelacion, reagendamiento, recordatorio';
COMMENT ON COLUMN notificaciones.estado IS 'Estado del envío: pendiente, enviada, fallida';
COMMENT ON COLUMN notificaciones.intentos_envio IS 'Número de intentos de envío realizados';

-- Trigger para actualizar fecha_modificacion
CREATE OR REPLACE FUNCTION update_notificaciones_modificacion()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_modificacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_notificaciones_modificacion
    BEFORE UPDATE ON notificaciones
    FOR EACH ROW
    EXECUTE FUNCTION update_notificaciones_modificacion();
