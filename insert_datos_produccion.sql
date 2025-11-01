-- ====================================================================
-- SCRIPT DE INSERCIÓN DE DATOS PARA PRODUCCIÓN
-- Sistema de Reservas - Conectemos Chile
-- ====================================================================
-- Este script contiene todos los datos maestros necesarios para
-- el funcionamiento del sistema en producción (VPS).
-- ====================================================================

-- Configuración inicial
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

BEGIN;

-- ====================================================================
-- 1. DATOS GEOGRÁFICOS
-- ====================================================================

-- Regiones de Chile
INSERT INTO regiones (nombre_region, codigo_region, id_region) VALUES
('Región Metropolitana de Santiago', 'RM', 1),
('Región de Valparaíso', 'V', 2),
('Región del Biobío', 'VIII', 3),
('Región de La Araucanía', 'IX', 4),
('Región de Los Lagos', 'X', 5),
('Región de Antofagasta', 'II', 6),
('Región de Atacama', 'III', 7),
('Región de Coquimbo', 'IV', 8),
('Región del Libertador General Bernardo O''Higgins', 'VI', 9),
('Región del Maule', 'VII', 10);

-- Ciudades principales
INSERT INTO ciudades (id_region, nombre_ciudad, id_ciudad) VALUES
(1, 'Santiago', 1),
(1, 'Puente Alto', 2),
(1, 'Maipú', 3),
(1, 'Las Condes', 4),
(1, 'La Florida', 5),
(1, 'Peñalolén', 6),
(1, 'San Bernardo', 7),
(1, 'Ñuñoa', 8),
(1, 'Providencia', 9),
(2, 'Valparaíso', 10),
(2, 'Viña del Mar', 11),
(2, 'Quilpué', 12),
(2, 'Villa Alemana', 13),
(3, 'Concepción', 14),
(3, 'Talcahuano', 15),
(3, 'Chillán', 16),
(3, 'Los Ángeles', 17),
(4, 'Temuco', 18),
(4, 'Villarrica', 19),
(4, 'Pucón', 20),
(5, 'Puerto Montt', 21),
(5, 'Osorno', 22),
(5, 'Castro', 23),
(6, 'Antofagasta', 24),
(7, 'Copiapó', 25),
(8, 'La Serena', 26),
(9, 'Rancagua', 27),
(10, 'Talca', 28);

-- ====================================================================
-- 2. ESPECIALIDADES Y PREVISIONES
-- ====================================================================

-- Especialidades psicológicas
INSERT INTO especialidades (nombre_especialidad, descripcion, id_especialidad) VALUES
('Psicología Clínica', 'Diagnóstico y tratamiento de trastornos mentales y emocionales', 1),
('Psicología Infantil', 'Especialización en niños y adolescentes', 2),
('Psicología de Pareja', 'Terapia y orientación para parejas', 3),
('Psicología Familiar', 'Intervención sistémica familiar', 4),
('Terapia Cognitivo-Conductual', 'Enfoque en cogniciones y comportamientos', 5),
('Psicoanálisis', 'Terapia psicoanalítica profunda', 6),
('Terapia Gestalt', 'Enfoque humanista y gestáltico', 7),
('Neuropsicología', 'Evaluación y rehabilitación neuropsicológica', 8),
('Psicología Organizacional', 'Intervención en contextos laborales', 9),
('Adicciones', 'Tratamiento de dependencias y adicciones', 10);

-- Previsiones de salud
INSERT INTO previsiones (nombre_prevision, id_prevision) VALUES
('FONASA A', 1),
('FONASA B', 2),
('FONASA C', 3),
('FONASA D', 4),
('ISAPRE Banmédica', 5),
('ISAPRE Colmena', 6),
('ISAPRE Cruz Blanca', 7),
('ISAPRE Consalud', 8),
('ISAPRE Vida Tres', 9),
('CAPREDENA', 10),
('DIPRECA', 11),
('Particular', 12);

-- ====================================================================
-- 3. SERVICIOS Y ESTADOS DE CITA
-- ====================================================================

-- Servicios disponibles
INSERT INTO servicios (nombre_servicio, descripcion, duracion_minutos, precio, tipo_servicio, estado, id_servicio) VALUES
('Consulta Individual Adultos', 'Sesión de terapia individual para adultos', 50, 45000.00, 'individual', 'activo', 1),
('Consulta Individual Niños/Adolescentes', 'Sesión de terapia individual para menores', 50, 40000.00, 'individual', 'activo', 2),
('Terapia de Pareja', 'Sesión de terapia para parejas', 60, 60000.00, 'pareja', 'activo', 3),
('Terapia Familiar', 'Sesión de terapia familiar sistémica', 60, 65000.00, 'familiar', 'activo', 4),
('Evaluación Psicológica', 'Evaluación psicológica completa', 90, 80000.00, 'evaluacion', 'activo', 5),
('Evaluación Neuropsicológica', 'Evaluación neuropsicológica especializada', 120, 120000.00, 'evaluacion', 'activo', 6),
('Primera Consulta', 'Primera consulta de evaluación e ingreso', 60, 50000.00, 'inicial', 'activo', 7);

-- Estados de cita
INSERT INTO estados_cita (nombre_estado, descripcion, color_hex, orden, id_estado_cita) VALUES
('agendada', 'Cita recién agendada, pendiente de confirmación', '#FFA500', 1, 1),
('confirmada', 'Cita confirmada por el paciente', '#008000', 2, 2),
('en_curso', 'Cita en desarrollo', '#0000FF', 3, 3),
('completada', 'Cita finalizada exitosamente', '#800080', 4, 4),
('cancelada_paciente', 'Cancelada por el paciente', '#FF0000', 5, 5),
('cancelada_profesional', 'Cancelada por el profesional', '#FF4500', 6, 6),
('no_asistio', 'Paciente no asistió a la cita', '#8B0000', 7, 7),
('reagendada', 'Cita reagendada para nueva fecha', '#DAA520', 8, 8);

-- ====================================================================
-- 4. SALAS DE ATENCIÓN
-- ====================================================================

INSERT INTO salas_atencion (nombre_sala, ubicacion, capacidad, equipamiento, estado, id_sala) VALUES
('Sala 1 - Adultos', 'Primer piso, ala norte', 2, 'Escritorio, 2 sillas, diván terapéutico, aire acondicionado', 'disponible', 1),
('Sala 2 - Infantil', 'Primer piso, ala sur', 4, 'Mesa infantil, juguetes terapéuticos, pizarra, cámaras', 'disponible', 2),
('Sala 3 - Parejas', 'Segundo piso, ala norte', 3, 'Mesa redonda, 3 sillas cómodas, sistema de audio', 'disponible', 3),
('Sala 4 - Familiar', 'Segundo piso, ala sur', 6, 'Sofás modulares, mesa de centro, sistema audiovisual', 'disponible', 4),
('Sala 5 - Evaluación', 'Primer piso, centro', 2, 'Escritorio amplio, computador, tests psicológicos', 'disponible', 5);

-- ====================================================================
-- 5. ROLES Y USUARIOS
-- ====================================================================

-- Roles del sistema
INSERT INTO roles (nombre_rol, descripcion, id_rol) VALUES
('administrador', 'Acceso completo al sistema', 1),
('psicologo', 'Profesional de salud mental', 2),
('recepcionista', 'Personal administrativo y atención al cliente', 3),
('supervisor', 'Supervisor clínico con acceso a reportes', 4);

-- Usuario administrador principal
-- Contraseña: 15935700 (debe cambiarse en producción)
INSERT INTO usuarios (nombre_usuario, email, estado, intentos_fallidos, id_usuario, contrasena) VALUES
('admin', 'admin@conectemoschile.cl', 'activo', 0, 1, '$2b$12$ZI/6jkCleTGL1zawa47XF.8LHMg4SEU2VLPZwbkMG6LWzekJv3VCi');

-- Asignar rol de administrador
INSERT INTO usuarios_roles (id_usuario, id_rol) VALUES (1, 1);

-- ====================================================================
-- 6. PSICÓLOGOS DE EJEMPLO (DATOS DE PRUEBA)
-- ====================================================================
-- NOTA: Estos son datos ficticios. Reemplazar con datos reales en producción.

-- Usuarios para psicólogos (Contraseña: ConectemosCL2025!)
INSERT INTO usuarios (nombre_usuario, email, estado, intentos_fallidos, id_usuario, contrasena) VALUES
('psi.rodriguez', 'ana.rodriguez@conectemoschile.cl', 'activo', 0, 2, '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNi2D.Y1O3K9K'),
('psi.martinez', 'carlos.martinez@conectemoschile.cl', 'activo', 0, 3, '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNi2D.Y1O3K9K'),
('psi.gonzalez', 'luis.gonzalez@conectemoschile.cl', 'activo', 0, 4, '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNi2D.Y1O3K9K'),
('psi.silva', 'maria.silva@conectemoschile.cl', 'activo', 0, 5, '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNi2D.Y1O3K9K'),
('psi.torres', 'patricia.torres@conectemoschile.cl', 'activo', 0, 6, '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNi2D.Y1O3K9K');

-- Datos de psicólogos
INSERT INTO psicologos (rut, nombres, apellido_paterno, apellido_materno, fecha_nacimiento, telefono, email_personal, direccion, registro_profesional, titulo_profesional, universidad, anios_experiencia, estado, id_usuario, id_psicologo) VALUES
('12345678-9', 'Ana María', 'Rodríguez', 'Silva', '1985-03-15', '+56912345678', 'ana.rodriguez.personal@gmail.com', 'Av. Providencia 1234, Providencia', 'REG-PSI-001-2010', 'Psicóloga Clínica', 'Universidad de Chile', 14, 'activo', 2, 1),
('12345679-0', 'Carlos Alberto', 'Martínez', 'López', '1982-07-22', '+56912345679', 'carlos.martinez.personal@gmail.com', 'Calle Las Condes 567, Las Condes', 'REG-PSI-002-2008', 'Psicólogo Infantil', 'Pontificia Universidad Católica de Chile', 16, 'activo', 3, 2),
('12345681-2', 'Luis Fernando', 'González', 'Morales', '1980-05-30', '+56912345681', 'luis.gonzalez.personal@gmail.com', 'Calle Apoquindo 123, Las Condes', 'REG-PSI-004-2006', 'Psicólogo Clínico', 'Universidad de Santiago', 18, 'activo', 4, 3),
('12345680-1', 'María Isabel', 'Silva', 'Fernández', '1988-11-08', '+56912345680', 'maria.silva.personal@gmail.com', 'Av. Las Condes 890, Las Condes', 'REG-PSI-003-2012', 'Psicóloga de Pareja y Familia', 'Universidad Diego Portales', 12, 'activo', 5, 4),
('12345682-3', 'Patricia Andrea', 'Torres', 'Ramírez', '1990-09-12', '+56912345682', 'patricia.torres.personal@gmail.com', 'Av. Providencia 567, Providencia', 'REG-PSI-005-2013', 'Neuropsicóloga', 'Universidad Católica', 11, 'activo', 6, 5);

-- Asignar rol de psicólogo a todos los psicólogos
INSERT INTO usuarios_roles (id_usuario, id_rol) VALUES
(2, 2), (3, 2), (4, 2), (5, 2), (6, 2);

-- ====================================================================
-- 7. HORARIOS DISPONIBLES DE PSICÓLOGOS
-- ====================================================================
-- Horarios de lunes a viernes (9:00-18:00) y sábados (9:00-13:00)

-- Psicólogo 1: Ana Rodríguez
INSERT INTO horarios_disponibles (dia_semana, hora_inicio, hora_fin, disponible, fecha_desde, id_psicologo) VALUES
('lunes', '09:00:00', '18:00:00', true, '2025-01-01', 1),
('martes', '09:00:00', '18:00:00', true, '2025-01-01', 1),
('miercoles', '09:00:00', '18:00:00', true, '2025-01-01', 1),
('jueves', '09:00:00', '18:00:00', true, '2025-01-01', 1),
('viernes', '09:00:00', '17:00:00', true, '2025-01-01', 1),
('sabado', '09:00:00', '13:00:00', true, '2025-01-01', 1);

-- Psicólogo 2: Carlos Martínez
INSERT INTO horarios_disponibles (dia_semana, hora_inicio, hora_fin, disponible, fecha_desde, id_psicologo) VALUES
('lunes', '09:00:00', '18:00:00', true, '2025-01-01', 2),
('martes', '09:00:00', '18:00:00', true, '2025-01-01', 2),
('miercoles', '09:00:00', '18:00:00', true, '2025-01-01', 2),
('jueves', '09:00:00', '18:00:00', true, '2025-01-01', 2),
('viernes', '09:00:00', '17:00:00', true, '2025-01-01', 2),
('sabado', '09:00:00', '13:00:00', true, '2025-01-01', 2);

-- Psicólogo 3: Luis González
INSERT INTO horarios_disponibles (dia_semana, hora_inicio, hora_fin, disponible, fecha_desde, id_psicologo) VALUES
('lunes', '09:00:00', '18:00:00', true, '2025-01-01', 3),
('martes', '09:00:00', '18:00:00', true, '2025-01-01', 3),
('miercoles', '09:00:00', '18:00:00', true, '2025-01-01', 3),
('jueves', '09:00:00', '18:00:00', true, '2025-01-01', 3),
('viernes', '09:00:00', '17:00:00', true, '2025-01-01', 3),
('sabado', '09:00:00', '13:00:00', true, '2025-01-01', 3);

-- Psicólogo 4: María Silva
INSERT INTO horarios_disponibles (dia_semana, hora_inicio, hora_fin, disponible, fecha_desde, id_psicologo) VALUES
('lunes', '09:00:00', '18:00:00', true, '2025-01-01', 4),
('martes', '09:00:00', '18:00:00', true, '2025-01-01', 4),
('miercoles', '09:00:00', '18:00:00', true, '2025-01-01', 4),
('jueves', '09:00:00', '18:00:00', true, '2025-01-01', 4),
('viernes', '09:00:00', '17:00:00', true, '2025-01-01', 4),
('sabado', '09:00:00', '13:00:00', true, '2025-01-01', 4);

-- Psicólogo 5: Patricia Torres
INSERT INTO horarios_disponibles (dia_semana, hora_inicio, hora_fin, disponible, fecha_desde, id_psicologo) VALUES
('lunes', '09:00:00', '18:00:00', true, '2025-01-01', 5),
('martes', '09:00:00', '18:00:00', true, '2025-01-01', 5),
('miercoles', '09:00:00', '18:00:00', true, '2025-01-01', 5),
('jueves', '09:00:00', '18:00:00', true, '2025-01-01', 5),
('viernes', '09:00:00', '17:00:00', true, '2025-01-01', 5),
('sabado', '09:00:00', '13:00:00', true, '2025-01-01', 5);

-- ====================================================================
-- 8. ACTUALIZAR SECUENCIAS
-- ====================================================================

SELECT setval('regiones_id_region_seq', 10, true);
SELECT setval('ciudades_id_ciudad_seq', 28, true);
SELECT setval('especialidades_id_especialidad_seq', 10, true);
SELECT setval('previsiones_id_prevision_seq', 12, true);
SELECT setval('servicios_id_servicio_seq', 7, true);
SELECT setval('estados_cita_id_estado_cita_seq', 8, true);
SELECT setval('salas_atencion_id_sala_seq', 5, true);
SELECT setval('roles_id_rol_seq', 4, true);
SELECT setval('usuarios_id_usuario_seq', 6, true);
SELECT setval('psicologos_id_psicologo_seq', 5, true);

COMMIT;

-- ====================================================================
-- SCRIPT COMPLETADO
-- ====================================================================
-- CREDENCIALES IMPORTANTES:
--
-- Usuario Admin:
--   - Usuario: admin
--   - Email: admin@conectemoschile.cl
--   - Contraseña: 15935700
--
-- Usuarios Psicólogos (todos con la misma contraseña temporal):
--   - Contraseña: ConectemosCL2025!
--
-- IMPORTANTE: Cambiar todas las contraseñas en producción
-- ====================================================================
