// API Client for Booking System
import { OpenAPI } from "./core/OpenAPI"

export interface Servicio {
  id_servicio: number
  nombre_servicio: string
  descripcion: string | null
  duracion_minutos: number
  precio: number
  tipo_servicio: string | null
  estado: string
}

export interface Psicologo {
  id_empleado: number
  id_usuario: number
  rut: string
  nombres: string
  apellido_paterno: string
  apellido_materno: string | null
  fecha_nacimiento: string
  telefono: string | null
  email_personal: string | null
  registro_profesional: string
  titulo_profesional: string | null
  universidad: string | null
  anios_experiencia: number | null
  estado: string
  fecha_registro: string
}

export interface ReservaCreate {
  rut: string
  nombres: string
  apellido_paterno: string
  apellido_materno?: string | null
  telefono: string
  email: string
  fecha_nacimiento: string
  id_servicio: number
  id_empleado: number
  fecha_cita: string
  hora_inicio: string
  hora_fin: string
  motivo_consulta?: string | null
}

export interface ReservaResponse {
  message: string
  codigo_confirmacion: string
  id_cita: number
  fecha_cita: string
  hora_inicio: string
}

export interface Cita {
  id_cita: number
  id_paciente: number
  id_empleado: number
  id_servicio: number
  id_sala: number | null
  id_estado_cita: number
  fecha_cita: string
  hora_inicio: string
  hora_fin: string
  motivo_consulta: string | null
  observaciones: string | null
  recordatorio_enviado: boolean
  codigo_confirmacion: string | null
  google_calendar_event_id: string | null
  fecha_creacion: string
  fecha_modificacion: string | null
}

export interface ReagendarRequest {
  nueva_fecha: string
  nueva_hora_inicio: string
  nueva_hora_fin: string
}

export interface ReagendarResponse {
  message: string
  codigo_confirmacion: string
  nueva_fecha: string
  nueva_hora_inicio: string
}

export interface HorarioDisponibilidadInfo {
  hora: string
  disponible: boolean
  ocupado: boolean
  pasado: boolean
}

export interface CitasPublic {
  data: Cita[]
  count: number
}

// API Functions
export const BookingService = {
  // GET /servicios
  async getServicios(): Promise<Servicio[]> {
    const response = await fetch(`${OpenAPI.BASE}/api/v1/servicios`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })

    if (!response.ok) {
      throw new Error("Error al obtener servicios")
    }

    return response.json()
  },

  // GET /empleados/disponibles
  async getPsicologosDisponibles(especialidadId?: number): Promise<Psicologo[]> {
    const url = new URL(`${OpenAPI.BASE}/api/v1/empleados/disponibles`)
    if (especialidadId) {
      url.searchParams.append("especialidad_id", especialidadId.toString())
    }

    const response = await fetch(url.toString(), {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })

    if (!response.ok) {
      throw new Error("Error al obtener psicólogos")
    }

    return response.json()
  },

  // GET /empleados/disponibilidad
  async getDisponibilidad(
    psicologoId: number,
    fecha: string,
  ): Promise<HorarioDisponibilidadInfo[]> {
    const url = new URL(`${OpenAPI.BASE}/api/v1/empleados/disponibilidad`)
    url.searchParams.append("psicologo_id", psicologoId.toString())
    url.searchParams.append("fecha", fecha)

    const response = await fetch(url.toString(), {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })

    if (!response.ok) {
      throw new Error("Error al obtener disponibilidad")
    }

    return response.json()
  },

  // POST /citas
  async crearReserva(reserva: ReservaCreate): Promise<ReservaResponse> {
    const response = await fetch(`${OpenAPI.BASE}/api/v1/citas`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(reserva),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || "Error al crear reserva")
    }

    return response.json()
  },

  // GET /citas/{codigo_confirmacion}
  async getCitaPorCodigo(codigoConfirmacion: string): Promise<Cita> {
    const response = await fetch(
      `${OpenAPI.BASE}/api/v1/citas/${codigoConfirmacion}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      },
    )

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || "Cita no encontrada")
    }

    return response.json()
  },

  // PUT /citas/{codigo_confirmacion}/reagendar
  async reagendarCita(
    codigoConfirmacion: string,
    datos: ReagendarRequest,
  ): Promise<ReagendarResponse> {
    const response = await fetch(
      `${OpenAPI.BASE}/api/v1/citas/${codigoConfirmacion}/reagendar`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(datos),
      },
    )

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || "Error al reagendar cita")
    }

    return response.json()
  },

  // DELETE /citas/{codigo_confirmacion}/cancelar
  async cancelarCita(codigoConfirmacion: string): Promise<{ message: string }> {
    const response = await fetch(
      `${OpenAPI.BASE}/api/v1/citas/${codigoConfirmacion}/cancelar`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      },
    )

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || "Error al cancelar cita")
    }

    return response.json()
  },

  // PUT /citas/{id}/confirmar (Para recepcionista)
  async confirmarCita(
    idCita: number,
  ): Promise<{ message: string; id_cita: number; estado: string }> {
    const token = await OpenAPI.TOKEN()
    const response = await fetch(
      `${OpenAPI.BASE}/api/v1/citas/${idCita}/confirmar`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      },
    )

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || "Error al confirmar cita")
    }

    return response.json()
  },

  // GET /citas/pendientes/lista (Para recepcionista)
  async getCitasPendientes(
    skip: number = 0,
    limit: number = 100,
  ): Promise<CitasPublic> {
    const token = await OpenAPI.TOKEN()
    const url = new URL(`${OpenAPI.BASE}/api/v1/citas/pendientes/lista`)
    url.searchParams.append("skip", skip.toString())
    url.searchParams.append("limit", limit.toString())

    const response = await fetch(url.toString(), {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    })

    if (!response.ok) {
      throw new Error("Error al obtener citas pendientes")
    }

    return response.json()
  },
}
