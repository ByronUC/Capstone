-- Migration: Add 'paciente_presente' state to estados_cita
-- Date: 2025-01-09
-- Description: Adds a new state to notify psychologist when patient arrives for appointment

-- Insert new state 'paciente_presente' between 'confirmada' and 'en_curso'
-- First, update orden for existing states to make room
UPDATE estados_cita
SET orden = orden + 1
WHERE orden >= 3;

-- Insert the new state
INSERT INTO estados_cita (nombre_estado, descripcion, color_identificador, orden)
VALUES (
    'paciente_presente',
    'Paciente presente en sala de espera',
    '#00CED1',  -- Dark Turquoise
    3
);

-- Update existing states order for clarity:
-- 1. agendada
-- 2. confirmada
-- 3. paciente_presente (NEW)
-- 4. en_curso
-- 5. completada
-- 6. cancelada_paciente
-- 7. cancelada_profesional
-- 8. no_asistio
-- 9. reagendada

COMMENT ON COLUMN estados_cita.nombre_estado IS 'Estado de la cita: agendada, confirmada, paciente_presente, en_curso, completada, cancelada_paciente, cancelada_profesional, no_asistio, reagendada';
