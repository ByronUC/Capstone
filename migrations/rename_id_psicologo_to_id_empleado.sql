-- Migration: Rename id_psicologo to id_empleado across all tables
-- Date: 2025-01-09
-- Description: Renames all id_psicologo columns to id_empleado for consistency

-- 1. Rename primary key in psicologos table
ALTER TABLE psicologos
RENAME COLUMN id_psicologo TO id_empleado;

-- 2. Rename foreign key in citas table
ALTER TABLE citas
RENAME COLUMN id_psicologo TO id_empleado;

-- 3. Rename foreign key in historial_clinico table
ALTER TABLE historial_clinico
RENAME COLUMN id_psicologo TO id_empleado;

-- 4. Rename foreign key in horarios_disponibles table
ALTER TABLE horarios_disponibles
RENAME COLUMN id_psicologo TO id_empleado;

-- 5. Rename foreign key in psicologos_especialidades table
ALTER TABLE psicologos_especialidades
RENAME COLUMN id_psicologo TO id_empleado;

-- 6. Rename foreign key in seguimientos table
ALTER TABLE seguimientos
RENAME COLUMN id_psicologo TO id_empleado;

-- 7. Rename foreign key in sesiones_clinicas table
ALTER TABLE sesiones_clinicas
RENAME COLUMN id_psicologo TO id_empleado;

-- 8. Rename foreign key in tratamientos table
ALTER TABLE tratamientos
RENAME COLUMN id_psicologo TO id_empleado;

-- Note: Foreign key constraints and sequences are automatically updated by PostgreSQL
-- The sequence psicologos_id_psicologo_seq will need to be renamed

ALTER SEQUENCE psicologos_id_psicologo_seq RENAME TO psicologos_id_empleado_seq;
