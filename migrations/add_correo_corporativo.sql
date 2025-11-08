-- Migration: Add corporate email field to usuarios table
-- Date: 2025-11-04
-- Description: Adds email_corporativo field to allow assigning corporate emails to psychologists

-- Add email_corporativo column
ALTER TABLE usuarios
ADD COLUMN IF NOT EXISTS email_corporativo VARCHAR(100);

-- Add index for performance
CREATE INDEX IF NOT EXISTS idx_usuarios_email_corporativo ON usuarios(email_corporativo);

-- Add comment
COMMENT ON COLUMN usuarios.email_corporativo IS 'Correo corporativo asignado al usuario (principalmente para psicólogos)';
