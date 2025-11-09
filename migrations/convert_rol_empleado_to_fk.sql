-- Migration: Convert rol_empleado from VARCHAR to foreign key reference to roles table
-- Date: 2025-01-09
-- Description: Changes rol_empleado from text field to integer foreign key referencing roles.id_rol

-- Step 1: Add new column id_rol as INTEGER (nullable temporarily)
ALTER TABLE psicologos
ADD COLUMN id_rol INTEGER;

-- Step 2: Map existing rol_empleado values to roles.id_rol
-- Mapping:
--   'psicologo' -> 2 (id_rol for psicologo)
--   'administrativo' -> 3 (id_rol for recepcionista, closest match)
--   'supervisor' -> 4 (id_rol for supervisor)
--   'otro' -> 2 (default to psicologo)

UPDATE psicologos
SET id_rol = CASE
    WHEN rol_empleado = 'psicologo' THEN 2
    WHEN rol_empleado = 'administrativo' THEN 3
    WHEN rol_empleado = 'supervisor' THEN 4
    WHEN rol_empleado = 'otro' THEN 2
    ELSE 2  -- Default to psicologo
END;

-- Step 3: Make id_rol NOT NULL now that all rows have values
ALTER TABLE psicologos
ALTER COLUMN id_rol SET NOT NULL;

-- Step 4: Add foreign key constraint
ALTER TABLE psicologos
ADD CONSTRAINT psicologos_id_rol_fkey
FOREIGN KEY (id_rol) REFERENCES roles(id_rol);

-- Step 5: Drop old rol_empleado column
ALTER TABLE psicologos
DROP COLUMN rol_empleado;

-- Step 6: Add comment explaining the column
COMMENT ON COLUMN psicologos.id_rol IS 'Rol del empleado en la organización (referencia a tabla roles)';
