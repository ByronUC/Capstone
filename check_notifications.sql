-- Verificar las últimas notificaciones creadas
SELECT 
    n.id_notificacion,
    n.id_cita,
    n.email_destinatario,
    n.tipo_notificacion,
    n.estado,
    n.intentos_envio,
    n.fecha_enviada,
    n.error_mensaje,
    c.fecha_cita,
    c.hora_inicio
FROM notificaciones n
JOIN citas c ON n.id_cita = c.id_cita
ORDER BY n.id_notificacion DESC
LIMIT 10;

-- Verificar si existen notificaciones para psicólogos
SELECT 
    tipo_notificacion,
    COUNT(*) as cantidad,
    SUM(CASE WHEN estado = 'enviada' THEN 1 ELSE 0 END) as enviadas,
    SUM(CASE WHEN estado = 'pendiente' THEN 1 ELSE 0 END) as pendientes,
    SUM(CASE WHEN estado = 'fallida' THEN 1 ELSE 0 END) as fallidas
FROM notificaciones
GROUP BY tipo_notificacion
ORDER BY tipo_notificacion;

-- Verificar psicólogos con email_personal
SELECT 
    id_psicologo,
    nombres,
    apellido_paterno,
    email_personal
FROM psicologos
WHERE email_personal IS NOT NULL;
