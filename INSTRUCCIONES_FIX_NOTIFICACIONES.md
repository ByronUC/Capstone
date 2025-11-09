# Fix para Error de Notificaciones en VPS

## Problema Identificado

El sistema está fallando con el error:
```
psycopg.errors.UndefinedColumn: record "new" has no field "fecha_modificacion"
```

**Causa**: Existe un trigger en PostgreSQL que intenta actualizar el campo `fecha_modificacion` en la tabla `notificaciones`, pero este campo no existe en el modelo Python de SQLModel.

## Solución

### Paso 1: Subir el script de migración al VPS

Desde tu máquina local, copia el archivo de migración al VPS:

```bash
scp migrations/fix_notificaciones_trigger.sql root@tu-servidor:~/Capstone/migrations/
```

### Paso 2: Conectarse al VPS

```bash
ssh root@tu-servidor
cd ~/Capstone
```

### Paso 3: Ejecutar el script de corrección

Opción A - Usando docker compose exec:
```bash
docker compose exec db psql -U postgres -d app -f /migrations/fix_notificaciones_trigger.sql
```

Opción B - Copiando el archivo al contenedor primero:
```bash
docker cp migrations/fix_notificaciones_trigger.sql capstone-db-1:/tmp/fix.sql
docker compose exec db psql -U postgres -d app -f /tmp/fix.sql
```

Opción C - Ejecutar línea por línea:
```bash
docker compose exec db psql -U postgres -d app
```

Luego ejecutar en el prompt de psql:
```sql
DROP TRIGGER IF EXISTS trigger_notificaciones_modificacion ON notificaciones;
DROP FUNCTION IF EXISTS update_notificaciones_modificacion();
ALTER TABLE notificaciones DROP COLUMN IF EXISTS fecha_modificacion;
\q
```

### Paso 4: Verificar que se corrigió

```bash
# Verificar la estructura de la tabla
docker compose exec db psql -U postgres -d app -c "\d notificaciones"
```

Deberías ver que ya no existe el campo `fecha_modificacion` ni el trigger.

### Paso 5: Reiniciar el backend

```bash
docker compose restart backend
```

### Paso 6: Verificar logs

```bash
docker compose logs -f backend
```

Deberías ver que el backend se inicia sin errores y las citas se pueden crear correctamente.

## Verificación de Funcionamiento

Intenta crear una cita desde el frontend. Ahora debería funcionar sin el error de `fecha_modificacion`.

**Nota sobre el error de email**: El mensaje "Error al enviar email: [Errno 101] Network is unreachable" es un problema diferente relacionado con la configuración de email/SMTP, pero ya no debería causar un crash del sistema.

## Próximos pasos (opcional)

Si deseas que las notificaciones tengan un campo de fecha de modificación, deberías:

1. Agregar el campo al modelo Python en `backend/app/models.py`
2. Crear una migración de Alembic apropiada
3. El trigger no es necesario ya que SQLModel/SQLAlchemy puede manejar esto automáticamente

## Comandos adicionales útiles

```bash
# Ver logs en tiempo real
docker compose logs -f backend

# Ver estado de todos los contenedores
docker compose ps

# Revisar la base de datos directamente
docker compose exec db psql -U postgres -d app

# Hacer backup antes de cambios importantes
docker compose exec db pg_dump -U postgres app > backup_$(date +%Y%m%d_%H%M%S).sql
```
