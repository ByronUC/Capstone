# Fix para Errores CORS en VPS

## Problema Identificado

Estás accediendo a la aplicación directamente por IP y puerto (`http://147.182.240.177:5173`), pero el sistema está configurado para usar Traefik como proxy reverso con dominios.

**Errores observados:**
1. CORS bloqueando peticiones de puerto 5173 a puerto 8000
2. Redirecciones 307 sin headers CORS apropiados

## Soluciones Disponibles

### ✅ **Opción 1: Usar Traefik (RECOMENDADO para producción)**

Esta es la forma correcta de acceder a la aplicación en producción.

#### Paso 1: Configurar tu dominio o usar localhost

Si tienes un dominio (ej: `conectemoschile.com`), apuntalo a tu IP `147.182.240.177` con registros A:
```
@ -> 147.182.240.177
api -> 147.182.240.177
dashboard -> 147.182.240.177
```

Si NO tienes dominio, puedes usar la IP con `nip.io` (servicio gratuito que resuelve DNS):
```
147.182.240.177.nip.io
```

#### Paso 2: Modificar `.env` en el VPS

```bash
ssh root@tu-servidor
cd ~/Capstone
nano .env
```

Cambia estas líneas:

**Si tienes dominio:**
```env
DOMAIN=conectemoschile.com
FRONTEND_HOST=https://dashboard.conectemoschile.com
VITE_API_URL=https://api.conectemoschile.com
BACKEND_CORS_ORIGINS="https://dashboard.conectemoschile.com,https://api.conectemoschile.com"
```

**Si usas nip.io:**
```env
DOMAIN=147.182.240.177.nip.io
FRONTEND_HOST=https://dashboard.147.182.240.177.nip.io
VITE_API_URL=https://api.147.182.240.177.nip.io
BACKEND_CORS_ORIGINS="https://dashboard.147.182.240.177.nip.io,https://api.147.182.240.177.nip.io,http://dashboard.147.182.240.177.nip.io,http://api.147.182.240.177.nip.io"
```

#### Paso 3: Verificar que Traefik esté corriendo

```bash
docker compose -f docker-compose.traefik.yml up -d
docker compose ps
```

#### Paso 4: Reconstruir y reiniciar servicios

```bash
# Reconstruir frontend con nueva URL
docker compose build frontend

# Reiniciar todos los servicios
docker compose up -d --force-recreate

# Ver logs
docker compose logs -f backend frontend
```

#### Paso 5: Acceder a la aplicación

**Con dominio:**
- Frontend: `https://dashboard.conectemoschile.com`
- Backend API: `https://api.conectemoschile.com/docs`

**Con nip.io:**
- Frontend: `https://dashboard.147.182.240.177.nip.io`
- Backend API: `https://api.147.182.240.177.nip.io/docs`

---

### ✅ **Opción 2: Acceso directo por IP (Solo para desarrollo/testing)**

Si prefieres seguir accediendo por IP y puertos directos sin Traefik:

#### Paso 1: Modificar docker-compose.yml

En tu VPS, edita `docker-compose.yml`:

```bash
ssh root@tu-servidor
cd ~/Capstone
nano docker-compose.yml
```

Agrega exposición de puertos al backend y frontend:

```yaml
  backend:
    # ... líneas existentes ...
    ports:
      - "8000:8000"  # Agregar esta línea

  frontend:
    # ... líneas existentes ...
    ports:
      - "5173:80"  # Agregar esta línea
```

#### Paso 2: Actualizar .env

```bash
nano .env
```

```env
DOMAIN=147.182.240.177
FRONTEND_HOST=http://147.182.240.177:5173
VITE_API_URL=http://147.182.240.177:8000
BACKEND_CORS_ORIGINS="http://147.182.240.177:5173,http://147.182.240.177:8000,http://147.182.240.177,http://localhost:5173"
ENVIRONMENT=local
```

#### Paso 3: Reconstruir y reiniciar

```bash
docker compose down
docker compose build
docker compose up -d
docker compose logs -f backend
```

#### Paso 4: Verificar CORS en logs

Deberías ver en los logs del backend algo como:
```
INFO: CORS origins: ['http://147.182.240.177:5173', 'http://147.182.240.177:8000']
```

---

### ✅ **Opción 3: Fix rápido temporal (Solo pruebas)**

Si solo quieres probar rápidamente sin cambiar configuraciones:

#### Paso 1: Agregar origen CORS amplio (NO SEGURO para producción)

```bash
ssh root@tu-servidor
cd ~/Capstone
```

Edita `backend/app/main.py` temporalmente:

```python
# Reemplaza la sección CORS con:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # PERMITIR TODO - SOLO PRUEBAS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Luego:
```bash
docker compose restart backend
```

⚠️ **IMPORTANTE**: Esta configuración permite CUALQUIER origen. Úsala SOLO para pruebas rápidas y luego vuelve a la configuración segura.

---

## Verificación de Funcionamiento

### Test de CORS
```bash
# Desde tu máquina local
curl -H "Origin: http://147.182.240.177:5173" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     http://147.182.240.177:8000/api/v1/citas/ -v
```

Deberías ver en la respuesta:
```
< Access-Control-Allow-Origin: http://147.182.240.177:5173
< Access-Control-Allow-Credentials: true
```

### Test de API
```bash
curl http://147.182.240.177:8000/api/v1/utils/health-check/
```

Debería devolver: `{"status":"ok"}`

---

## Recomendación Final

Para producción, usa **Opción 1** con un dominio real o con nip.io. Es más seguro, profesional y maneja HTTPS automáticamente con Let's Encrypt.

La configuración actual de tu proyecto ya está preparada para esto, solo necesitas ajustar las variables de entorno y usar Traefik correctamente.

---

## Troubleshooting

### Si aún ves errores CORS:

1. **Verifica que el backend recibió las variables:**
```bash
docker compose exec backend env | grep CORS
```

2. **Revisa los logs del backend:**
```bash
docker compose logs backend | grep -i cors
```

3. **Limpia caché del navegador:**
- Abre DevTools (F12)
- Click derecho en el botón de recargar
- Selecciona "Vaciar caché y recargar de manera forzada"

4. **Verifica headers en Network tab:**
- Abre DevTools → Network
- Mira la petición fallida
- Verifica que los headers `Access-Control-*` estén presentes en la respuesta

### Si el error persiste:

```bash
# Ver configuración actual del backend
docker compose exec backend python -c "from app.core.config import settings; print(f'CORS Origins: {settings.all_cors_origins}')"

# Reiniciar todo limpio
docker compose down
docker compose up -d
docker compose logs -f
```
