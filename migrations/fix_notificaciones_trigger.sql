-- Migración: Corregir trigger de notificaciones
-- Fecha: 2025-11-01
-- Problema: El trigger intenta actualizar fecha_modificacion que no existe en el modelo Python

-- 1. Eliminar el trigger existente
DROP TRIGGER IF EXISTS trigger_notificaciones_modificacion ON notificaciones;

-- 2. Eliminar la función del trigger
DROP FUNCTION IF EXISTS update_notificaciones_modificacion();

-- 3. Eliminar la columna fecha_modificacion si existe (ya que no está en el modelo Python)
ALTER TABLE notificaciones DROP COLUMN IF EXISTS fecha_modificacion;

-- Verificación
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'notificaciones' 
ORDER BY ordinal_position;
