# CONTEXTO DEL PROYECTO: Sistema de Reservas - SIGC (Conectemos Chile)

## DESCRIPCIÓN GENERAL
Necesito desarrollar un sistema completo de gestión de citas para una clínica psicológica llamada "Conectemos Chile". El sistema debe permitir que pacientes agenden, reagenden y cancelen citas online, y que recepcionistas confirmen estas citas desde una aplicación de escritorio.

---

## COMPONENTES DEL SISTEMA

### 1. APLICACIÓN WEB (Para Pacientes)

#### Formulario de Reserva de Cita
- Página con formulario que capture:
  - **Datos del paciente:** nombre completo, RUT, email, teléfono
  - **Selector de tipo de servicio** (terapia individual, pareja, infantil, etc.)
  - **Calendario interactivo** que muestre:
    - Mes actual con días habilitados/deshabilitados
    - Al hacer clic en un día, debe cargar las horas disponibles
    - Días sin disponibilidad deben aparecer visualmente bloqueados
  - **Lista de horarios disponibles** para el día seleccionado (botones clickeables)
  - **Campo de motivo de consulta** (textarea)
  - **Botón "Confirmar Reserva"**

#### Funcionalidad de Reagendar Cita
- Formulario donde el paciente ingresa su **código de confirmación**
- Al validar el código, mostrar:
  - Información de su cita actual (fecha, hora, psicólogo, servicio)
  - Botón "Reagendar"
- Al clickear "Reagendar":
  - Mostrar calendario de disponibilidad nuevamente
  - Permitir seleccionar nueva fecha y hora
  - Botón "Confirmar reagendamiento"

#### Funcionalidad de Cancelar Cita
- Formulario donde el paciente ingresa su **código de confirmación**
- Al validar el código, mostrar:
  - Información de su cita
  - Botón "Cancelar Cita" (con confirmación)
- Mensaje de éxito al cancelar

---

### 2. API BACKEND (FastAPI)

#### Endpoints Necesarios

**GET /api/servicios**
- Retorna lista de todos los servicios disponibles de la clínica
- Respuesta: array de objetos con `id_servicio`, `nombre_servicio`, `descripcion`, `duracion`, `precio`

**GET /api/psicologos/disponibles?especialidad_id={id}**
- Retorna psicólogos que ofrecen esa especialidad
- Respuesta: array con `id_psicologo`, `nombres`, `apellidos`, `especialidades`

**GET /api/disponibilidad?psicologo_id={id}&fecha={YYYY-MM-DD}**
- Calcula y retorna horarios disponibles para ese psicólogo en esa fecha
- **Lógica:**
  1. Consultar tabla `horarios_disponibles` del psicólogo para ese día de semana
  2. Generar array de horarios posibles (intervalos de 1 hora)
  3. Consultar tabla `citas` para ver horarios ya ocupados en esa fecha
  4. Restar ocupados de disponibles
- Respuesta: array de strings con horarios `["09:00", "10:00", "11:00"]`

**POST /api/citas**
- Crea una nueva cita
- Body: `datos_paciente`, `id_servicio`, `id_psicologo`, `fecha`, `hora_inicio`, `hora_fin`, `motivo`
- **Lógica:**
  1. Validar que el horario siga disponible (double-check)
  2. Insertar/actualizar paciente en tabla `pacientes`
  3. Insertar cita en tabla `citas` con estado "Pendiente"
  4. Generar código único de confirmación (UUID)
  5. Asignar sala automáticamente
  6. Crear registro en tabla `notificaciones` para enviar email
- Respuesta: código de confirmación

**GET /api/citas/{codigo_confirmacion}**
- Busca y retorna información de una cita por su código
- Respuesta: datos completos de la cita

**PUT /api/citas/{codigo_confirmacion}/reagendar**
- Reagenda una cita existente
- Body: `nueva_fecha`, `nueva_hora_inicio`, `nueva_hora_fin`
- **Lógica:**
  1. Buscar cita por código
  2. Validar nueva disponibilidad
  3. Actualizar fecha y hora de la cita
  4. Cambiar estado a "Reprogramada"
  5. Crear notificación de reagendamiento
  6. Si existe `google_calendar_event_id`, actualizar evento en Google Calendar
- Respuesta: confirmación con nuevos datos

**DELETE /api/citas/{codigo_confirmacion}/cancelar**
- Cancela una cita
- **Lógica:**
  1. Buscar cita por código
  2. Actualizar estado a "Cancelada"
  3. Liberar horario (no aparecerá como ocupado)
  4. Crear notificaciones de cancelación
  5. Si existe `google_calendar_event_id`, eliminar evento de Google Calendar
- Respuesta: confirmación de cancelación

**PUT /api/citas/{id}/confirmar**
- Endpoint para que recepcionista confirme una cita (desde app escritorio)
- **Lógica:**
  1. Actualizar estado de "Pendiente" a "Confirmada"
  2. Crear notificaciones para paciente y psicólogo
  3. Crear evento en Google Calendar
  4. Guardar `google_calendar_event_id` en la cita
- Respuesta: confirmación

---

### 3. APLICACIÓN DE ESCRITORIO (Para Recepcionista)

#### Panel de Citas Pendientes
- Tabla que muestre todas las citas con estado "Pendiente"
- **Columnas:** Fecha, Hora, Nombre Paciente, Teléfono, Email, Servicio, Psicólogo
- **Botones por fila:**
  - "Confirmar" (botón verde)
  - "Rechazar" (botón rojo)
  
#### Acción Confirmar
- Al hacer clic en "Confirmar":
  1. Llamar a endpoint `PUT /api/citas/{id}/confirmar`
  2. Mostrar loading mientras procesa
  3. Actualizar lista de citas pendientes
  4. Mostrar mensaje de éxito

---

### 4. INTEGRACIÓN CON GOOGLE CALENDAR

#### Configuración
- Usar **Google Calendar API**
- Credenciales OAuth 2.0 o Service Account
- Una cuenta de Google Calendar para la clínica

#### Funcionalidades

**Crear evento al confirmar cita:**
- **Título:** "Cita - [Nombre Paciente] - [Servicio]"
- **Fecha y hora de inicio**
- **Fecha y hora de fin**
- **Descripción:** Datos del paciente y motivo
- **Asistentes:** email del psicólogo y del paciente
- **Recordatorio:** 24 horas antes
- Guardar el `event_id` retornado en BD

**Actualizar evento al reagendar:**
- Usar el `google_calendar_event_id` guardado
- Actualizar fecha y hora del evento existente

**Eliminar evento al cancelar:**
- Usar el `google_calendar_event_id` guardado
- Eliminar el evento de Google Calendar

---

### 5. SISTEMA DE NOTIFICACIONES POR EMAIL

#### Servicio SMTP
- Configurar servidor SMTP (Gmail, SendGrid, etc.)
- Credenciales en variables de entorno

#### Templates de Email

**Confirmación inicial (Estado: Pendiente):**
```
Asunto: Solicitud de cita recibida - Conectemos Chile

Hola [Nombre],
Hemos recibido tu solicitud de cita.

Código de confirmación: [CODIGO]
Fecha: [FECHA]
Hora: [HORA]
Psicólogo: [NOMBRE_PSICOLOGO]

Estado: Pendiente de confirmación por recepción
```

**Confirmación final (Estado: Confirmada):**
```
Asunto: Cita confirmada - Conectemos Chile

Hola [Nombre],
Tu cita ha sido confirmada.

Fecha: [FECHA]
Hora: [HORA]
Psicólogo: [NOMBRE_PSICOLOGO]
Dirección: [DIRECCION_CLINICA]
```

**Recordatorio (24h antes):**
```
Asunto: Recordatorio de cita - Mañana

Hola [Nombre],
Te recordamos tu cita para mañana:

Fecha: [FECHA]
Hora: [HORA]
Psicólogo: [NOMBRE_PSICOLOGO]
```

**Cancelación:**
```
Asunto: Cita cancelada - Conectemos Chile

Hola [Nombre],
Tu cita ha sido cancelada.

Si deseas agendar nuevamente, visita [URL]
```

**Reagendamiento:**
```
Asunto: Cita reagendada - Conectemos Chile

Hola [Nombre],
Tu cita ha sido reagendada.

Nueva fecha: [FECHA]
Nueva hora: [HORA]
```

#### Proceso de envío
- Backend inserta registro en tabla `notificaciones`
- Worker/Scheduler procesa cola de notificaciones
- Actualiza estado a "Enviada" o "Fallida"
- Si falla, reintenta hasta 3 veces

---

## ESTRUCTURA DE BASE DE DATOS

### Tablas Principales Involucradas

**pacientes:**
- `id_paciente` (PK)
- `rut`
- `nombres`
- `apellido_paterno`
- `apellido_materno`
- `telefono`
- `email`
- `fecha_nacimiento`
- `consentimiento_informado`
- `fecha_consentimiento`

**psicologos:**
- `id_psicologo` (PK)
- `nombres`
- `apellidos`
- `email`
- `registro_profesional`

**psicologos_especialidades:**
- `id_psicologo` (FK)
- `id_especialidad` (FK)

**especialidades:**
- `id_especialidad` (PK)
- `nombre_especialidad`

**servicios:**
- `id_servicio` (PK)
- `nombre_servicio`
- `descripcion`
- `duracion_minutos`
- `precio`

**horarios_disponibles:**
- `id_horario` (PK)
- `id_psicologo` (FK)
- `dia_semana`
- `hora_inicio`
- `hora_fin`
- `disponible`

**estados_cita:**
- `id_estado_cita` (PK)
- `nombre_estado` (Pendiente, Confirmada, Realizada, Cancelada, Reprogramada)

**citas:**
- `id_cita` (PK)
- `id_paciente` (FK)
- `id_psicologo` (FK)
- `id_servicio` (FK)
- `id_sala` (FK)
- `id_estado_cita` (FK)
- `fecha_cita`
- `hora_inicio`
- `hora_fin`
- `motivo_consulta`
- `observaciones`
- `codigo_confirmacion` (UNIQUE)
- `google_calendar_event_id` **(NUEVO CAMPO A AGREGAR)**
- `fecha_creacion`
- `fecha_modificacion`

**salas_atencion:**
- `id_sala` (PK)
- `nombre_sala`
- `estado`

**notificaciones:**
- `id_notificacion` (PK)
- `email_destinatario`
- `tipo_notificacion`
- `asunto`
- `contenido`
- `estado` (pendiente, enviada, fallida)
- `fecha_programada`
- `fecha_enviada`

---

## LÓGICA DE NEGOCIO CLAVE

### Calcular Disponibilidad
1. Consultar `horarios_disponibles` del psicólogo para el día de semana solicitado
2. Generar array de horarios posibles (09:00, 10:00, 11:00, etc.)
3. Consultar `citas` existentes para ese psicólogo en esa fecha con estados activos
4. Filtrar horarios ocupados
5. Retornar solo horarios libres

### Asignar Sala Automáticamente
1. Consultar `salas_atencion` con estado "disponible"
2. Verificar que no esté ocupada en ese horario (consultar `citas`)
3. Asignar la primera sala disponible

### Validar Disponibilidad (Evitar doble reserva)
- Siempre validar justo antes de confirmar
- Usar transacciones en BD
- Lock de fila si es necesario

### Generar Código de Confirmación
- Usar UUID único
- Formato: XXX-XXX-XXX o similar
- Almacenar en campo `codigo_confirmacion`

---

## FLUJOS COMPLETOS

### Flujo 1: Paciente Agenda Nueva Cita
1. Paciente entra al formulario web
2. Selecciona servicio → sistema muestra psicólogos con esa especialidad
3. Selecciona fecha en calendario → sistema consulta disponibilidad
4. Sistema muestra horarios libres del día
5. Paciente selecciona horario y completa datos
6. Click "Confirmar reserva"
7. Backend valida disponibilidad
8. Backend crea/actualiza paciente
9. Backend inserta cita con estado "Pendiente"
10. Backend genera código único
11. Backend crea notificación email
12. Sistema muestra página de confirmación con código
13. Email enviado al paciente

### Flujo 2: Recepcionista Confirma Cita
1. Recepcionista ve cita en panel de "Pendientes"
2. Revisa datos del paciente
3. Click en botón "Confirmar"
4. Backend actualiza estado a "Confirmada"
5. Backend crea evento en Google Calendar
6. Backend guarda event_id en BD
7. Backend crea notificaciones para paciente y psicólogo
8. Emails enviados
9. Panel actualiza lista

### Flujo 3: Paciente Cancela Cita
1. Paciente ingresa código de confirmación
2. Sistema busca y muestra datos de la cita
3. Paciente click "Cancelar cita"
4. Sistema solicita confirmación
5. Backend actualiza estado a "Cancelada"
6. Backend elimina evento de Google Calendar
7. Backend crea notificaciones
8. Sistema muestra mensaje de éxito

### Flujo 4: Paciente Reagenda Cita
1. Paciente ingresa código de confirmación
2. Sistema muestra cita actual
3. Paciente click "Reagendar"
4. Sistema muestra calendario de disponibilidad
5. Paciente selecciona nueva fecha y hora
6. Backend valida disponibilidad
7. Backend actualiza cita con nueva fecha/hora
8. Backend actualiza evento en Google Calendar
9. Backend crea notificaciones
10. Sistema muestra confirmación

---

## CONSIDERACIONES TÉCNICAS

### Seguridad
- Códigos de confirmación deben ser únicos (UUID)
- Validar que el código existe antes de permitir acciones
- Recepcionista debe autenticarse con rol específico
- No exponer IDs internos de BD al público

### Performance
- Indexar campo `codigo_confirmacion` en tabla `citas`
- Indexar `fecha_cita` y `id_psicologo` para consultas rápidas
- Cachear lista de servicios (no cambia frecuentemente)

### Concurrencia
- Usar transacciones en BD para evitar doble reserva
- Validar disponibilidad justo antes de confirmar (no confiar solo en frontend)

### Resiliencia
- Si falla email, reintentar automáticamente (max 3 intentos)
- Si falla Google Calendar, no bloquear el flujo principal
- Logs detallados de todas las operaciones críticas

### Variables de Entorno Necesarias
```env
DATABASE_URL=postgresql://...
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=...
SMTP_PASSWORD=...
GOOGLE_CALENDAR_CREDENTIALS_PATH=...
GOOGLE_CALENDAR_ID=...
FRONTEND_URL=https://...
```

---

## TECNOLOGÍAS A USAR

- **Backend:** FastAPI (Python)
- **Base de Datos:** PostgreSQL
- **Frontend Web:** React o HTML/CSS/JS vanilla
- **App Escritorio:** Electron o similar
- **Email:** SMTP (Gmail/SendGrid)
- **Calendar:** Google Calendar API
- **Librerías útiles:**
  - Backend: SQLAlchemy, Pydantic, python-jose (JWT), passlib
  - Email: smtplib o python-emailer
  - Google: google-auth, google-api-python-client

---

## CAMBIOS NECESARIOS EN BD

```sql
-- Agregar campo para Google Calendar
ALTER TABLE citas 
ADD COLUMN google_calendar_event_id VARCHAR(255);

-- Índice para búsqueda rápida por código
CREATE INDEX idx_citas_codigo ON citas(codigo_confirmacion);
```

---

## PRIORIDADES DE DESARROLLO

1. ✅ API endpoints básicos (servicios, disponibilidad, crear cita)
2. ✅ Formulario web de reserva
3. ✅ Sistema de confirmación por recepcionista
4. ✅ Sistema de notificaciones email
5. ✅ Funcionalidad de cancelar/reagendar
6. ✅ Integración con Google Calendar
7. ✅ Recordatorios automáticos (24h antes)

---

## RESULTADO ESPERADO

Un sistema completo donde:
- ✅ Pacientes pueden agendar citas 24/7 desde web
- ✅ Ven disponibilidad real en tiempo real
- ✅ Reciben código de confirmación por email
- ✅ Pueden cancelar o reagendar usando su código
- ✅ Recepcionista confirma citas desde app escritorio
- ✅ Se envían emails automáticos en cada paso
- ✅ Las citas confirmadas se crean automáticamente en Google Calendar
- ✅ Todo queda registrado en base de datos