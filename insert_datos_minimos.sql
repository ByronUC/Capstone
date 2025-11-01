-- ============================================
-- DATOS MÍNIMOS PARA SISTEMA DE RESERVAS
-- Solo inserta lo necesario para que funcione el formulario de reserva
-- ============================================

-- 1. VERIFICAR Y CREAR USUARIO ADMIN SI NO EXISTE
INSERT INTO usuarios (nombre_usuario, contrasena, email, estado, intentos_fallidos, fecha_creacion)
SELECT 'admin_temp', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNi2D.Y1O3K9K', 'admin.temp@conectemoschile.cl', 'activo', 0, CURRENT_TIMESTAMP
WHERE NOT EXISTS (SELECT 1 FROM usuarios WHERE nombre_usuario = 'admin_temp');

-- 2. CREAR USUARIOS PARA PSICÓLOGOS (5 psicólogos)
INSERT INTO usuarios (nombre_usuario, contrasena, email, estado, intentos_fallidos, fecha_creacion)
SELECT * FROM (VALUES
    ('psi.rodriguez', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNi2D.Y1O3K9K', 'ana.rodriguez@conectemoschile.cl', 'activo', 0, CURRENT_TIMESTAMP),
    ('psi.martinez', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNi2D.Y1O3K9K', 'carlos.martinez@conectemoschile.cl', 'activo', 0, CURRENT_TIMESTAMP),
    ('psi.silva', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNi2D.Y1O3K9K', 'maria.silva@conectemoschile.cl', 'activo', 0, CURRENT_TIMESTAMP),
    ('psi.gonzalez', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNi2D.Y1O3K9K', 'luis.gonzalez@conectemoschile.cl', 'activo', 0, CURRENT_TIMESTAMP),
    ('psi.torres', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNi2D.Y1O3K9K', 'patricia.torres@conectemoschile.cl', 'activo', 0, CURRENT_TIMESTAMP)
) AS datos(nombre_usuario, contrasena, email, estado, intentos_fallidos, fecha_creacion)
WHERE NOT EXISTS (
    SELECT 1 FROM usuarios WHERE nombre_usuario = datos.nombre_usuario
);

-- 3. CREAR PSICÓLOGOS (usando los IDs de los usuarios recién creados)
INSERT INTO psicologos (id_usuario, rut, nombres, apellido_paterno, apellido_materno, fecha_nacimiento, telefono, email_personal, direccion, registro_profesional, titulo_profesional, universidad, anios_experiencia, estado, fecha_registro)
SELECT u.id_usuario, d.rut, d.nombres, d.apellido_paterno, d.apellido_materno, d.fecha_nacimiento::date, d.telefono, d.email_personal, d.direccion, d.registro_profesional, d.titulo_profesional, d.universidad, d.anios_experiencia, d.estado, CURRENT_TIMESTAMP
FROM usuarios u
CROSS JOIN (VALUES
    ('psi.rodriguez', '12345678-9', 'Ana María', 'Rodríguez', 'Silva', '1985-03-15', '+56912345678', 'ana.rodriguez.personal@gmail.com', 'Av. Providencia 1234, Providencia', 'REG-PSI-001-2010', 'Psicóloga Clínica', 'Universidad de Chile', 14, 'activo'),
    ('psi.martinez', '12345679-0', 'Carlos Alberto', 'Martínez', 'López', '1982-07-22', '+56912345679', 'carlos.martinez.personal@gmail.com', 'Calle Las Condes 567, Las Condes', 'REG-PSI-002-2008', 'Psicólogo Infantil', 'Pontificia Universidad Católica de Chile', 16, 'activo'),
    ('psi.silva', '12345680-1', 'María Isabel', 'Silva', 'Fernández', '1988-11-08', '+56912345680', 'maria.silva.personal@gmail.com', 'Av. Las Condes 890, Las Condes', 'REG-PSI-003-2012', 'Psicóloga de Pareja y Familia', 'Universidad Diego Portales', 12, 'activo'),
    ('psi.gonzalez', '12345681-2', 'Luis Fernando', 'González', 'Morales', '1980-05-30', '+56912345681', 'luis.gonzalez.personal@gmail.com', 'Calle Apoquindo 123, Las Condes', 'REG-PSI-004-2006', 'Psicólogo Clínico', 'Universidad de Santiago', 18, 'activo'),
    ('psi.torres', '12345682-3', 'Patricia Andrea', 'Torres', 'Ramírez', '1990-09-12', '+56912345682', 'patricia.torres.personal@gmail.com', 'Av. Providencia 567, Providencia', 'REG-PSI-005-2013', 'Neuropsicóloga', 'Universidad Católica', 11, 'activo')
) AS d(usuario, rut, nombres, apellido_paterno, apellido_materno, fecha_nacimiento, telefono, email_personal, direccion, registro_profesional, titulo_profesional, universidad, anios_experiencia, estado)
WHERE u.nombre_usuario = d.usuario
AND NOT EXISTS (
    SELECT 1 FROM psicologos WHERE id_usuario = u.id_usuario
);

-- 4. CREAR HORARIOS DISPONIBLES PARA CADA PSICÓLOGO
-- Para cada psicólogo, crear horarios de Lunes a Viernes
INSERT INTO horarios_disponibles (id_psicologo, dia_semana, hora_inicio, hora_fin, disponible, fecha_desde, observaciones)
SELECT p.id_psicologo, d.dia, d.hora_inicio::time, d.hora_fin::time, true, '2025-01-01'::date, 'Horario regular'
FROM psicologos p
CROSS JOIN (VALUES
    ('lunes', '09:00', '18:00'),
    ('martes', '09:00', '18:00'),
    ('miercoles', '09:00', '18:00'),
    ('jueves', '09:00', '18:00'),
    ('viernes', '09:00', '17:00')
) AS d(dia, hora_inicio, hora_fin)
WHERE NOT EXISTS (
    SELECT 1 FROM horarios_disponibles
    WHERE id_psicologo = p.id_psicologo AND dia_semana = d.dia
);

-- 5. VERIFICAR QUE LOS SERVICIOS EXISTEN (ya están insertados según el log)
-- Si no existen, crearlos
INSERT INTO servicios (nombre_servicio, descripcion, duracion_minutos, precio, tipo_servicio, estado, fecha_creacion)
SELECT * FROM (VALUES
    ('Consulta Individual Adultos', 'Sesión de terapia individual para adultos', 50, 45000.00, 'individual', 'activo', CURRENT_TIMESTAMP),
    ('Consulta Individual Niños/Adolescentes', 'Sesión de terapia individual para menores', 50, 40000.00, 'individual', 'activo', CURRENT_TIMESTAMP),
    ('Terapia de Pareja', 'Sesión de terapia para parejas', 60, 60000.00, 'pareja', 'activo', CURRENT_TIMESTAMP),
    ('Terapia Familiar', 'Sesión de terapia familiar sistémica', 60, 65000.00, 'familiar', 'activo', CURRENT_TIMESTAMP),
    ('Evaluación Psicológica', 'Evaluación psicológica completa', 90, 80000.00, 'evaluacion', 'activo', CURRENT_TIMESTAMP)
) AS datos(nombre_servicio, descripcion, duracion_minutos, precio, tipo_servicio, estado, fecha_creacion)
WHERE NOT EXISTS (
    SELECT 1 FROM servicios WHERE nombre_servicio = datos.nombre_servicio
);

-- VERIFICACIÓN FINAL
SELECT 'Usuarios creados:' as info, COUNT(*) as total FROM usuarios;
SELECT 'Psicólogos creados:' as info, COUNT(*) as total FROM psicologos;
SELECT 'Servicios disponibles:' as info, COUNT(*) as total FROM servicios WHERE estado = 'activo';
SELECT 'Horarios configurados:' as info, COUNT(*) as total FROM horarios_disponibles;
