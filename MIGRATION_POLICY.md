# Política de Migraciones de Base de Datos

## ⚠️ IMPORTANTE: NO USAR ALEMBIC AUTOGENERATE

Este proyecto utiliza **migraciones SQL manuales** exclusivamente. NO ejecutar comandos de Alembic autogenerate.

## ❌ Comandos Prohibidos

```bash
# NO EJECUTAR ESTOS COMANDOS:
alembic revision --autogenerate
docker exec capstone-backend-1 alembic revision --autogenerate
```

## ✅ Proceso Correcto para Migraciones

### 1. Crear archivo SQL de migración

Crear un nuevo archivo en `migrations/` con el siguiente formato de nombre:
```
migrations/descripcion_del_cambio.sql
```

Ejemplo:
```sql
-- Migration: Descripción clara del cambio
-- Date: YYYY-MM-DD
-- Description: Explicación detallada de qué hace esta migración

-- Cambios en el esquema
ALTER TABLE nombre_tabla
ADD COLUMN nueva_columna VARCHAR(100);

-- Comentarios explicativos
COMMENT ON COLUMN nombre_tabla.nueva_columna IS 'Descripción del propósito de la columna';
```

### 2. Ejecutar la migración en el servidor

Desde tu máquina local, conectarte al VPS y ejecutar:

```bash
# Copiar el archivo SQL al contenedor
ssh root@147.182.240.177 "cd /root/Capstone && docker compose cp migrations/tu_migracion.sql db:/tmp/"

# Ejecutar la migración
ssh root@147.182.240.177 "cd /root/Capstone && docker compose exec -T db psql -U postgres -d app -f /tmp/tu_migracion.sql"
```

### 3. Actualizar modelos de Python

Después de ejecutar la migración SQL, actualizar los modelos en:
- `backend/app/models.py`
- Archivos de rutas en `backend/app/api/routes/`

### 4. Actualizar interfaces de TypeScript (si aplica)

Si el cambio afecta el frontend, actualizar:
- `frontend/src/client/booking.ts`
- Otros archivos TypeScript que usen las interfaces afectadas

### 5. Reiniciar servicios

```bash
ssh root@147.182.240.177 "cd /root/Capstone && docker compose restart backend"
```

## 🔍 Verificar Estado de la Base de Datos

Para verificar columnas específicas:
```bash
ssh root@147.182.240.177 "cd /root/Capstone && docker compose exec -T db psql -U postgres -d app -c \"SELECT table_name, column_name FROM information_schema.columns WHERE column_name = 'nombre_columna' ORDER BY table_name;\""
```

## 📋 Historial de Migraciones Aplicadas

| Fecha | Archivo | Descripción |
|-------|---------|-------------|
| 2025-01-08 | `add_rol_empleado.sql` | Agregado campo rol_empleado a tabla psicologos |
| 2025-01-09 | `rename_id_psicologo_to_id_empleado.sql` | Renombrado id_psicologo a id_empleado en 8 tablas |

## ⚠️ Problema Conocido: Alembic Autogenerate

Si accidentalmente se ejecuta `alembic revision --autogenerate`, Alembic intentará generar migraciones que reviertan los cambios manuales porque no tiene registro de las migraciones SQL.

**Solución si esto ocurre:**

1. NO aplicar la migración generada
2. Eliminar el archivo de migración generado en `backend/app/alembic/versions/`
3. Limpiar el estado de Alembic:
   ```bash
   ssh root@147.182.240.177 "cd /root/Capstone && docker compose exec -T db psql -U postgres -d app -c \"DELETE FROM alembic_version;\""
   ```
4. Verificar que la base de datos esté en el estado correcto
5. Continuar usando migraciones SQL manuales

## 📚 Razones para Usar Migraciones Manuales

1. **Control Total**: Sabemos exactamente qué SQL se ejecuta
2. **Compatibilidad**: No hay conflictos entre Alembic y cambios manuales
3. **Simplicidad**: No se requiere mantener dos sistemas de migración paralelos
4. **Historial Claro**: Archivos SQL legibles y versionados en Git
5. **Debugging Fácil**: Podemos ejecutar y probar el SQL directamente

## 🤝 Trabajo en Equipo

Si múltiples desarrolladores necesitan aplicar la misma migración:

1. Hacer commit del archivo `.sql` en Git
2. Cada desarrollador ejecuta el SQL en su entorno
3. Todos actualizan los modelos de Python siguiendo el mismo commit
4. Se mantiene la consistencia entre código y base de datos
