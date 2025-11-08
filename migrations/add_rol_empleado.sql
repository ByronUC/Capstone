-- Migration: Add rol_empleado field to psicologos table
-- Date: 2025-01-08
-- Description: Adds rol_empleado field to allow assigning different roles to employees (psicologo, administrativo, etc.)

-- Add rol_empleado column with default value 'psicologo'
ALTER TABLE psicologos
ADD COLUMN IF NOT EXISTS rol_empleado VARCHAR(50) DEFAULT 'psicologo';

-- Add comment
COMMENT ON COLUMN psicologos.rol_empleado IS 'Rol del empleado en la organización (psicologo, administrativo, supervisor, etc.)';

-- Update existing records to have 'psicologo' as default role
UPDATE psicologos
SET rol_empleado = 'psicologo'
WHERE rol_empleado IS NULL;
