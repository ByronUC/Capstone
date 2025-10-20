# Documentación de Endpoints API - Conectemos Chile

Esta documentación describe los endpoints REST API implementados para el sistema de gestión de Conectemos Chile.

## Base URL

Todos los endpoints están prefijados con: `/api/v1`

---

## 🏥 MÓDULO: PACIENTES

Base path: `/api/v1/pacientes`

### GET /pacientes
**Summary:** Obtener lista de pacientes

**Descripción:** Retorna lista de pacientes con historial médico básico, filtrable por nombre, DNI, estado (activo/inactivo) o tipo de tratamiento actual.

**Parámetros de consulta:**
- `skip` (int, opcional): Número de registros a omitir (default: 0)
- `limit` (int, opcional): Número máximo de registros a retornar (default: 100)

**Respuesta exitosa:** 200 OK
```json
{
  "data": [
    {
      "id_paciente": 1,
      "rut": "12.345.678-9",
      "nombres": "Juan Carlos",
      "apellido_paterno": "González",
      "apellido_materno": "López",
      "fecha_nacimiento": "1985-05-15",
      "genero": "masculino",
      "telefono": "+56912345678",
      "email": "juan.gonzalez@example.com",
      "direccion": "Av. Principal 123",
      "estado_civil": "casado",
      "ocupacion": "Ingeniero",
      "estado": "activo",
      "consentimiento_informado": true,
      "id_ciudad": 1,
      "id_prevision": 1,
      "fecha_registro": "2024-01-15T10:30:00"
    }
  ],
  "count": 1
}
```

### GET /pacientes/{id}
**Summary:** Obtener paciente por ID

**Descripción:** Retorna información completa del paciente incluyendo datos personales, antecedentes médicos, alergias, tratamientos activos, contacto de emergencia e historial de atención.

**Parámetros de ruta:**
- `id` (int, requerido): ID del paciente

**Respuesta exitosa:** 200 OK (mismo formato que objeto individual arriba)

**Errores:**
- 404 Not Found: El paciente no existe en el sistema

### POST /pacientes
**Summary:** Registrar nuevo paciente

**Descripción:** Registra un nuevo paciente con datos personales, antecedentes médicos relevantes, alergias conocidas, tipo de sangre y contacto de emergencia. Genera historial clínico inicial.

**Body de la petición:**
```json
{
  "rut": "12.345.678-9",
  "nombres": "Juan Carlos",
  "apellido_paterno": "González",
  "apellido_materno": "López",
  "fecha_nacimiento": "1985-05-15",
  "genero": "masculino",
  "telefono": "+56912345678",
  "email": "juan.gonzalez@example.com",
  "direccion": "Av. Principal 123",
  "estado_civil": "casado",
  "ocupacion": "Ingeniero",
  "consentimiento_informado": true,
  "id_ciudad": 1,
  "id_prevision": 1
}
```

**Respuesta exitosa:** 200 OK

**Errores:**
- 400 Bad Request: Ya existe un paciente con este RUT en el sistema

### PUT /pacientes/{id}
**Summary:** Actualizar paciente completo

**Descripción:** Actualiza toda la información del paciente incluyendo datos personales y antecedentes médicos completos.

**Parámetros de ruta:**
- `id` (int, requerido): ID del paciente

**Body:** Mismo formato que POST

**Errores:**
- 404 Not Found: El paciente no existe en el sistema
- 409 Conflict: Ya existe otro paciente con este RUT

### PATCH /pacientes/{id}
**Summary:** Actualizar paciente parcialmente

**Descripción:** Modifica campos específicos del registro del paciente como contacto, dirección, alergias o información de emergencia sin afectar el historial médico.

**Body:** Cualquier subconjunto de campos del modelo Paciente

**Errores:**
- 404 Not Found: El paciente no existe en el sistema
- 409 Conflict: Ya existe otro paciente con este RUT

### DELETE /pacientes/{id}
**Summary:** Dar de baja paciente

**Descripción:** Marca el paciente como inactivo en el sistema. Valida que no tenga tratamientos activos o citas programadas. No elimina físicamente para mantener historial médico.

**Respuesta exitosa:** 200 OK
```json
{
  "message": "Paciente dado de baja exitosamente"
}
```

**Errores:**
- 404 Not Found: Paciente no encontrado

---

## 📅 MÓDULO: CITAS

Base path: `/api/v1/citas`

### GET /citas
**Summary:** Obtener lista de citas

**Descripción:** Retorna citas programadas con filtros por fecha, estado (pendiente/confirmada/completada/cancelada), cliente o empleado asignado.

**Parámetros:**
- `skip` (int, opcional): Offset para paginación
- `limit` (int, opcional): Límite de resultados

### GET /citas/{id}
**Summary:** Obtener cita por ID

**Descripción:** Retorna detalles completos de una cita específica incluyendo cliente, empleado asignado, fecha, hora, duración, servicio solicitado, estado actual y observaciones.

### POST /citas
**Summary:** Crear nueva cita

**Descripción:** Crea una cita con fecha, hora, cliente, empleado asignado y servicio solicitado. Valida disponibilidad de horario del empleado y evita solapamiento de citas.

**Body de la petición:**
```json
{
  "fecha_cita": "2024-02-15",
  "hora_inicio": "10:00:00",
  "hora_fin": "11:00:00",
  "motivo_consulta": "Evaluación inicial",
  "observaciones": "Primera consulta",
  "id_paciente": 1,
  "id_psicologo": 1,
  "id_servicio": 1,
  "id_sala": 1,
  "id_estado_cita": 1,
  "recordatorio_enviado": false
}
```

### PUT /citas/{id}
**Summary:** Actualizar cita completa

**Descripción:** Modifica completamente los datos de una cita existente incluyendo reprogramación de fecha/hora.

### PATCH /citas/{id}
**Summary:** Actualizar estado de cita

**Descripción:** Actualiza campos específicos como estado (confirmar, cancelar, completar), observaciones o asignación de empleado.

### DELETE /citas/{id}
**Summary:** Cancelar y eliminar cita

**Descripción:** Cancela y elimina una cita del sistema. Libera el horario para nuevas citas.

---

## 💊 MÓDULO: TRATAMIENTOS

Base path: `/api/v1/tratamientos`

### GET /tratamientos
**Summary:** Obtener lista de tratamientos

**Descripción:** Retorna tratamientos médicos activos e históricos con filtros por paciente, tipo de tratamiento, medicación asociada, estado.

### GET /tratamientos/{id}
**Summary:** Obtener tratamiento por ID

**Descripción:** Retorna detalles completos del tratamiento incluyendo paciente, tipo, medicación asociada, duración estimada, médico responsable.

### POST /tratamientos
**Summary:** Crear nuevo tratamiento

**Body de la petición:**
```json
{
  "tipo_tratamiento": "Terapia cognitivo-conductual",
  "descripcion": "Tratamiento para ansiedad generalizada",
  "objetivos": "Reducir síntomas de ansiedad",
  "fecha_inicio": "2024-02-01",
  "fecha_fin_estimada": "2024-08-01",
  "estado": "activo",
  "id_paciente": 1,
  "id_psicologo": 1,
  "id_cita": 1
}
```

### PUT /tratamientos/{id}
**Summary:** Actualizar tratamiento completo

### PATCH /tratamientos/{id}
**Summary:** Actualizar tratamiento parcialmente

**Descripción:** Actualiza estado (suspender, reanudar, completar), añade observaciones médicas o ajusta dosis.

### DELETE /tratamientos/{id}
**Summary:** Finalizar y eliminar tratamiento

**Descripción:** Solo permitido si está completado o suspendido.

**Errores:**
- 400 Bad Request: Solo se pueden eliminar tratamientos completados o suspendidos

---

## 💉 MÓDULO: MEDICACIÓN

Base path: `/api/v1/medicacion`

### GET /medicacion
**Summary:** Obtener catálogo de medicamentos

**Descripción:** Retorna catálogo completo de medicamentos disponibles.

### GET /medicacion/{id}
**Summary:** Obtener medicamento por ID

### POST /medicacion
**Summary:** Añadir medicamento al catálogo

**Body de la petición:**
```json
{
  "nombre_medicamento": "Sertralina",
  "dosis": "50mg",
  "frecuencia": "1 vez al día",
  "via_administracion": "oral",
  "fecha_inicio": "2024-02-01",
  "fecha_fin": null,
  "prescrito_por": "Dr. María González",
  "observaciones": "Tomar con alimentos",
  "estado": "activo",
  "id_paciente": 1,
  "id_tratamiento": 1
}
```

### PUT /medicacion/{id}
**Summary:** Actualizar medicamento completo

### PATCH /medicacion/{id}
**Summary:** Actualizar medicamento parcialmente

### DELETE /medicacion/{id}
**Summary:** Eliminar medicamento del catálogo

**Errores:**
- 409 Conflict: El medicamento está asociado a tratamientos activos

---

## 📊 MÓDULO: SEGUIMIENTO

Base path: `/api/v1/seguimiento`

### GET /seguimiento
**Summary:** Obtener registros de seguimiento

**Descripción:** Retorna registros de seguimiento médico y de servicios con filtros por paciente, tipo de seguimiento.

### GET /seguimiento/{id}
**Summary:** Obtener seguimiento por ID

### POST /seguimiento
**Summary:** Crear registro de seguimiento

**Body de la petición:**
```json
{
  "fecha_seguimiento": "2024-02-15",
  "tipo_seguimiento": "control",
  "estado_animo": "estable",
  "nivel_funcionalidad": 7,
  "adherencia_tratamiento": "buena",
  "observaciones": "El paciente muestra mejoría significativa",
  "proxima_evaluacion": "2024-03-15",
  "id_paciente": 1,
  "id_psicologo": 1,
  "id_tratamiento": 1
}
```

### PUT /seguimiento/{id}
**Summary:** Actualizar seguimiento completo

### PATCH /seguimiento/{id}
**Summary:** Actualizar seguimiento parcialmente

**Descripción:** Añade nuevas observaciones médicas, actualiza estado del paciente o reprograma próxima cita.

### DELETE /seguimiento/{id}
**Summary:** Eliminar registro de seguimiento

**Descripción:** Solo permitido si fue creado por error y no tiene registros dependientes.

---

## Códigos de Estado HTTP Comunes

- **200 OK**: Operación exitosa
- **400 Bad Request**: Datos inválidos o violación de restricciones
- **404 Not Found**: Recurso no encontrado
- **409 Conflict**: Conflicto con el estado actual (ej: duplicado)
- **500 Internal Server Error**: Error del servidor

---

## Notas de Implementación

1. **Autenticación**: Los endpoints actualmente no requieren autenticación. Se recomienda implementar autenticación JWT en producción.

2. **Validaciones Pendientes**:
   - Validación de disponibilidad de horarios en citas
   - Validación de solapamiento de citas
   - Verificación de tratamientos activos antes de eliminar
   - Notificaciones por email

3. **Paginación**: Todos los endpoints GET de listado soportan paginación mediante los parámetros `skip` y `limit`.

4. **Filtrado**: Los filtros avanzados (por nombre, fecha, estado, etc.) están documentados pero deben implementarse según necesidad.

5. **Relaciones**: Los modelos tienen relaciones configuradas. Se puede expandir la respuesta para incluir objetos relacionados modificando los schemas.

---

## Documentación Interactiva

Una vez que el servidor esté corriendo, puedes acceder a la documentación interactiva de Swagger UI en:

```
http://localhost:8000/api/v1/docs
```

O la documentación alternativa de ReDoc en:

```
http://localhost:8000/api/v1/redoc
```

---

**Fecha de creación:** 2024-10-19
**Versión de API:** v1
**Framework:** FastAPI + SQLModel
