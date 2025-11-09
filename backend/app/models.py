import uuid
from datetime import date, datetime, time
from typing import Optional
from decimal import Decimal

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel, Column, String


# ============================================
# MODELOS DE AUTENTICACIÓN Y USUARIOS
# ============================================

# Tabla: usuarios
class UsuarioBase(SQLModel):
    nombre_usuario: str = Field(unique=True, index=True, max_length=50)
    email: EmailStr = Field(unique=True, index=True, max_length=100)
    estado: str = Field(default='activo', max_length=20)
    intentos_fallidos: int = Field(default=0)


class UsuarioCreate(UsuarioBase):
    contrasena: str = Field(min_length=8, max_length=40)


class UsuarioUpdate(SQLModel):
    nombre_usuario: str | None = Field(default=None, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=100)
    contrasena: str | None = Field(default=None, min_length=8, max_length=40)
    estado: str | None = Field(default=None, max_length=20)


class Usuario(UsuarioBase, table=True):
    __tablename__ = "usuarios"

    id_usuario: int | None = Field(default=None, primary_key=True)
    contrasena: str = Field(max_length=255)  # Hash bcrypt
    fecha_creacion: datetime | None = Field(default_factory=datetime.utcnow)
    fecha_ultima_sesion: datetime | None = None
    token_recuperacion: str | None = Field(default=None, max_length=255)
    fecha_expiracion_token: datetime | None = None

    # Relaciones
    roles: list["UsuarioRol"] = Relationship(back_populates="usuario", cascade_delete=True)
    psicologo: Optional["Psicologo"] = Relationship(back_populates="usuario", cascade_delete=True)
    citas_creadas: list["Cita"] = Relationship(back_populates="usuario_creador")
    notificaciones: list["Notificacion"] = Relationship(back_populates="usuario")


class UsuarioPublic(UsuarioBase):
    id_usuario: int
    fecha_creacion: datetime | None


class UsuariosPublic(SQLModel):
    data: list[UsuarioPublic]
    count: int


# Tabla: roles
class RolBase(SQLModel):
    nombre_rol: str = Field(unique=True, max_length=50)
    descripcion: str | None = None


class RolCreate(RolBase):
    pass


class Rol(RolBase, table=True):
    __tablename__ = "roles"

    id_rol: int | None = Field(default=None, primary_key=True)
    fecha_creacion: datetime | None = Field(default_factory=datetime.utcnow)

    # Relaciones
    usuarios: list["UsuarioRol"] = Relationship(back_populates="rol")


class RolPublic(RolBase):
    id_rol: int


# Tabla: usuarios_roles (Relación N:M)
class UsuarioRolBase(SQLModel):
    id_usuario: int = Field(foreign_key="usuarios.id_usuario")
    id_rol: int = Field(foreign_key="roles.id_rol")


class UsuarioRol(UsuarioRolBase, table=True):
    __tablename__ = "usuarios_roles"

    id_usuario_rol: int | None = Field(default=None, primary_key=True)
    fecha_asignacion: datetime | None = Field(default_factory=datetime.utcnow)

    # Relaciones
    usuario: Usuario = Relationship(back_populates="roles")
    rol: Rol = Relationship(back_populates="usuarios")


# ============================================
# MODELOS DE NORMALIZACIÓN
# ============================================

# Tabla: regiones
class RegionBase(SQLModel):
    nombre_region: str = Field(unique=True, max_length=100)
    codigo_region: str | None = Field(default=None, unique=True, max_length=10)


class Region(RegionBase, table=True):
    __tablename__ = "regiones"

    id_region: int | None = Field(default=None, primary_key=True)

    # Relaciones
    ciudades: list["Ciudad"] = Relationship(back_populates="region")


# Tabla: ciudades
class CiudadBase(SQLModel):
    id_region: int = Field(foreign_key="regiones.id_region")
    nombre_ciudad: str = Field(max_length=100)


class Ciudad(CiudadBase, table=True):
    __tablename__ = "ciudades"

    id_ciudad: int | None = Field(default=None, primary_key=True)

    # Relaciones
    region: Region = Relationship(back_populates="ciudades")
    pacientes: list["Paciente"] = Relationship(back_populates="ciudad")


class CiudadCreate(CiudadBase):
    pass


class CiudadUpdate(SQLModel):
    id_region: int | None = None
    nombre_ciudad: str | None = None


class CiudadPublic(CiudadBase):
    id_ciudad: int


class CiudadesPublic(SQLModel):
    data: list[CiudadPublic]
    count: int


# Tabla: especialidades
class EspecialidadBase(SQLModel):
    nombre_especialidad: str = Field(unique=True, max_length=100)
    descripcion: str | None = None


class Especialidad(EspecialidadBase, table=True):
    __tablename__ = "especialidades"

    id_especialidad: int | None = Field(default=None, primary_key=True)
    fecha_creacion: datetime | None = Field(default_factory=datetime.utcnow)

    # Relaciones
    psicologos: list["PsicologoEspecialidad"] = Relationship(back_populates="especialidad")


# Tabla: previsiones
class PrevisionBase(SQLModel):
    nombre_prevision: str = Field(unique=True, max_length=100)
    tipo: str | None = Field(default=None, max_length=50)


class Prevision(PrevisionBase, table=True):
    __tablename__ = "previsiones"

    id_prevision: int | None = Field(default=None, primary_key=True)

    # Relaciones
    pacientes: list["Paciente"] = Relationship(back_populates="prevision")


class PrevisionCreate(PrevisionBase):
    pass


class PrevisionUpdate(SQLModel):
    nombre_prevision: str | None = None
    tipo: str | None = None


class PrevisionPublic(PrevisionBase):
    id_prevision: int


class PrevisionesPublic(SQLModel):
    data: list[PrevisionPublic]
    count: int


# ============================================
# MODELOS DE PSICÓLOGOS
# ============================================

# Tabla: psicologos
class PsicologoBase(SQLModel):
    rut: str = Field(unique=True, max_length=12)
    nombres: str = Field(max_length=100)
    apellido_paterno: str = Field(max_length=50)
    apellido_materno: str | None = Field(default=None, max_length=50)
    fecha_nacimiento: date | None = None
    telefono: str | None = Field(default=None, max_length=20)
    email_personal: str | None = Field(default=None, max_length=100)
    direccion: str | None = None
    registro_profesional: str = Field(unique=True, max_length=50)
    titulo_profesional: str | None = Field(default=None, max_length=150)
    universidad: str | None = Field(default=None, max_length=150)
    anios_experiencia: int | None = None
    foto_perfil: str | None = Field(default=None, max_length=255)
    rol_empleado: str | None = Field(default='psicologo', max_length=50)
    estado: str = Field(default='activo', max_length=20)


class PsicologoCreate(PsicologoBase):
    id_usuario: int


class Psicologo(PsicologoBase, table=True):
    __tablename__ = "psicologos"

    id_empleado: int | None = Field(default=None, primary_key=True)
    id_usuario: int = Field(unique=True, foreign_key="usuarios.id_usuario")
    fecha_registro: datetime | None = Field(default_factory=datetime.utcnow)

    # Relaciones
    usuario: Usuario = Relationship(back_populates="psicologo")
    especialidades: list["PsicologoEspecialidad"] = Relationship(back_populates="psicologo", cascade_delete=True)
    horarios: list["HorarioDisponible"] = Relationship(back_populates="psicologo", cascade_delete=True)
    citas: list["Cita"] = Relationship(back_populates="psicologo")
    historiales: list["HistorialClinico"] = Relationship(back_populates="psicologo")
    tratamientos: list["Tratamiento"] = Relationship(back_populates="psicologo")
    seguimientos: list["Seguimiento"] = Relationship(back_populates="psicologo")
    sesiones: list["SesionClinica"] = Relationship(back_populates="psicologo")


class PsicologoPublic(PsicologoBase):
    id_empleado: int
    id_usuario: int
    fecha_registro: datetime | None = None


class PsicologoUpdate(SQLModel):
    rut: str | None = Field(default=None, max_length=12)
    nombres: str | None = Field(default=None, max_length=100)
    apellido_paterno: str | None = Field(default=None, max_length=50)
    apellido_materno: str | None = Field(default=None, max_length=50)
    fecha_nacimiento: date | None = None
    telefono: str | None = Field(default=None, max_length=20)
    email_personal: str | None = Field(default=None, max_length=100)
    direccion: str | None = None
    registro_profesional: str | None = Field(default=None, max_length=50)
    titulo_profesional: str | None = Field(default=None, max_length=150)
    universidad: str | None = Field(default=None, max_length=150)
    anios_experiencia: int | None = None
    foto_perfil: str | None = Field(default=None, max_length=255)
    rol_empleado: str | None = Field(default=None, max_length=50)
    estado: str | None = Field(default=None, max_length=20)


class PsicologosPublic(SQLModel):
    data: list[PsicologoPublic]
    count: int


# Tabla: psicologos_especialidades (Relación N:M)
class PsicologoEspecialidadBase(SQLModel):
    id_empleado: int = Field(foreign_key="psicologos.id_empleado")
    id_especialidad: int = Field(foreign_key="especialidades.id_especialidad")
    fecha_certificacion: date | None = None
    institucion_certificadora: str | None = Field(default=None, max_length=150)
    vigente: bool = Field(default=True)


class PsicologoEspecialidad(PsicologoEspecialidadBase, table=True):
    __tablename__ = "psicologos_especialidades"

    id_psicologo_especialidad: int | None = Field(default=None, primary_key=True)

    # Relaciones
    psicologo: Psicologo = Relationship(back_populates="especialidades")
    especialidad: Especialidad = Relationship(back_populates="psicologos")


# ============================================
# MODELOS DE PACIENTES
# ============================================

# Tabla: pacientes
class PacienteBase(SQLModel):
    rut: str = Field(unique=True, max_length=12)
    nombres: str = Field(max_length=100)
    apellido_paterno: str = Field(max_length=50)
    apellido_materno: str | None = Field(default=None, max_length=50)
    fecha_nacimiento: date
    genero: str | None = Field(default=None, max_length=20)
    telefono: str = Field(max_length=20)
    email: str | None = Field(default=None, max_length=100)
    direccion: str | None = None
    estado_civil: str | None = Field(default=None, max_length=30)
    ocupacion: str | None = Field(default=None, max_length=100)
    estado: str = Field(default='activo', max_length=20)
    consentimiento_informado: bool = Field(default=False)


class PacienteCreate(PacienteBase):
    id_ciudad: int | None = None
    id_prevision: int | None = None


class PacienteUpdate(SQLModel):
    rut: str | None = Field(default=None, max_length=12)
    nombres: str | None = Field(default=None, max_length=100)
    apellido_paterno: str | None = Field(default=None, max_length=50)
    apellido_materno: str | None = Field(default=None, max_length=50)
    fecha_nacimiento: date | None = None
    genero: str | None = Field(default=None, max_length=20)
    telefono: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=100)
    direccion: str | None = None
    estado_civil: str | None = Field(default=None, max_length=30)
    ocupacion: str | None = Field(default=None, max_length=100)
    estado: str | None = Field(default=None, max_length=20)
    consentimiento_informado: bool | None = None
    id_ciudad: int | None = None
    id_prevision: int | None = None


class Paciente(PacienteBase, table=True):
    __tablename__ = "pacientes"

    id_paciente: int | None = Field(default=None, primary_key=True)
    id_ciudad: int | None = Field(default=None, foreign_key="ciudades.id_ciudad")
    id_prevision: int | None = Field(default=None, foreign_key="previsiones.id_prevision")
    fecha_registro: datetime | None = Field(default_factory=datetime.utcnow)
    fecha_consentimiento: datetime | None = None

    # Relaciones
    ciudad: Optional[Ciudad] = Relationship(back_populates="pacientes")
    prevision: Optional[Prevision] = Relationship(back_populates="pacientes")
    contactos_emergencia: list["ContactoEmergencia"] = Relationship(back_populates="paciente", cascade_delete=True)
    citas: list["Cita"] = Relationship(back_populates="paciente", cascade_delete=True)
    historiales: list["HistorialClinico"] = Relationship(back_populates="paciente", cascade_delete=True)
    antecedentes: list["AntecedenteMedico"] = Relationship(back_populates="paciente", cascade_delete=True)
    tratamientos: list["Tratamiento"] = Relationship(back_populates="paciente", cascade_delete=True)
    medicamentos: list["Medicamento"] = Relationship(back_populates="paciente", cascade_delete=True)
    seguimientos: list["Seguimiento"] = Relationship(back_populates="paciente", cascade_delete=True)
    sesiones: list["SesionClinica"] = Relationship(back_populates="paciente")


class PacientePublic(PacienteBase):
    id_paciente: int
    id_ciudad: int | None
    id_prevision: int | None
    fecha_registro: datetime


class PacientesPublic(SQLModel):
    data: list[PacientePublic]
    count: int


# Tabla: contactos_emergencia
class ContactoEmergenciaBase(SQLModel):
    nombre_completo: str = Field(max_length=100)
    telefono: str = Field(max_length=20)
    relacion: str | None = Field(default=None, max_length=50)
    es_principal: bool = Field(default=True)


class ContactoEmergencia(ContactoEmergenciaBase, table=True):
    __tablename__ = "contactos_emergencia"

    id_contacto_emergencia: int | None = Field(default=None, primary_key=True)
    id_paciente: int = Field(foreign_key="pacientes.id_paciente")
    fecha_registro: datetime | None = Field(default_factory=datetime.utcnow)

    # Relaciones
    paciente: Paciente = Relationship(back_populates="contactos_emergencia")


# ============================================
# MODELOS DE SERVICIOS Y RECURSOS
# ============================================

# Tabla: servicios
class ServicioBase(SQLModel):
    nombre_servicio: str = Field(max_length=150)
    descripcion: str | None = None
    duracion_minutos: int
    precio: Decimal = Field(max_digits=10, decimal_places=2)
    tipo_servicio: str | None = Field(default=None, max_length=50)
    estado: str = Field(default='activo', max_length=20)


class Servicio(ServicioBase, table=True):
    __tablename__ = "servicios"

    id_servicio: int | None = Field(default=None, primary_key=True)
    fecha_creacion: datetime | None = Field(default_factory=datetime.utcnow)

    # Relaciones
    citas: list["Cita"] = Relationship(back_populates="servicio")


class ServicioPublic(ServicioBase):
    id_servicio: int


class ServiciosPublic(SQLModel):
    data: list[ServicioPublic]
    count: int


# Tabla: salas_atencion
class SalaAtencionBase(SQLModel):
    nombre_sala: str = Field(max_length=50)
    ubicacion: str | None = Field(default=None, max_length=100)
    capacidad: int = Field(default=2)
    equipamiento: str | None = None
    estado: str = Field(default='disponible', max_length=20)


class SalaAtencion(SalaAtencionBase, table=True):
    __tablename__ = "salas_atencion"

    id_sala: int | None = Field(default=None, primary_key=True)
    fecha_creacion: datetime | None = Field(default_factory=datetime.utcnow)

    # Relaciones
    citas: list["Cita"] = Relationship(back_populates="sala")


# Tabla: horarios_disponibles
class HorarioDisponibleBase(SQLModel):
    dia_semana: str = Field(max_length=20)
    hora_inicio: time
    hora_fin: time
    disponible: bool = Field(default=True)
    fecha_desde: date | None = None
    fecha_hasta: date | None = None
    observaciones: str | None = None


class HorarioDisponible(HorarioDisponibleBase, table=True):
    __tablename__ = "horarios_disponibles"

    id_horario: int | None = Field(default=None, primary_key=True)
    id_empleado: int = Field(foreign_key="psicologos.id_empleado")

    # Relaciones
    psicologo: Psicologo = Relationship(back_populates="horarios")


# ============================================
# MODELOS DE CITAS
# ============================================

# Tabla: estados_cita
class EstadoCitaBase(SQLModel):
    nombre_estado: str = Field(unique=True, max_length=50)
    descripcion: str | None = None
    color_identificador: str | None = Field(default=None, max_length=7)
    orden: int | None = None


class EstadoCita(EstadoCitaBase, table=True):
    __tablename__ = "estados_cita"

    id_estado_cita: int | None = Field(default=None, primary_key=True)
    fecha_creacion: datetime | None = Field(default_factory=datetime.utcnow)

    # Relaciones
    citas: list["Cita"] = Relationship(back_populates="estado_cita")


# Tabla: citas
class CitaBase(SQLModel):
    fecha_cita: date
    hora_inicio: time
    hora_fin: time
    motivo_consulta: str | None = None
    observaciones: str | None = None
    recordatorio_enviado: bool = Field(default=False)


class CitaCreate(CitaBase):
    id_paciente: int
    id_empleado: int
    id_servicio: int
    id_sala: int | None = None
    id_estado_cita: int


class Cita(CitaBase, table=True):
    __tablename__ = "citas"

    id_cita: int | None = Field(default=None, primary_key=True)
    id_paciente: int = Field(foreign_key="pacientes.id_paciente")
    id_empleado: int = Field(foreign_key="psicologos.id_empleado")
    id_servicio: int = Field(foreign_key="servicios.id_servicio")
    id_sala: int | None = Field(default=None, foreign_key="salas_atencion.id_sala")
    id_estado_cita: int = Field(foreign_key="estados_cita.id_estado_cita")
    codigo_confirmacion: str | None = Field(default=None, unique=True, max_length=20)
    google_calendar_event_id: str | None = Field(default=None, max_length=255)
    fecha_creacion: datetime | None = Field(default_factory=datetime.utcnow)
    fecha_modificacion: datetime | None = None
    usuario_creacion: int | None = Field(default=None, foreign_key="usuarios.id_usuario")
    fecha_recordatorio: datetime | None = None

    # Relaciones
    paciente: Paciente = Relationship(back_populates="citas")
    psicologo: Psicologo = Relationship(back_populates="citas")
    servicio: Servicio = Relationship(back_populates="citas")
    sala: Optional[SalaAtencion] = Relationship(back_populates="citas")
    estado_cita: EstadoCita = Relationship(back_populates="citas")
    usuario_creador: Optional[Usuario] = Relationship(back_populates="citas_creadas")
    sesiones: list["SesionClinica"] = Relationship(back_populates="cita", cascade_delete=True)
    tratamientos: list["Tratamiento"] = Relationship(back_populates="cita")
    notificaciones: list["Notificacion"] = Relationship(back_populates="cita", cascade_delete=True)


class CitaPublic(CitaBase):
    id_cita: int
    id_paciente: int
    id_empleado: int
    id_servicio: int
    id_sala: int | None
    id_estado_cita: int
    codigo_confirmacion: str | None
    fecha_creacion: datetime
    fecha_modificacion: datetime | None


class CitasPublic(SQLModel):
    data: list[CitaPublic]
    count: int


class CitaUpdate(SQLModel):
    fecha_cita: date | None = None
    hora_inicio: time | None = None
    hora_fin: time | None = None
    motivo_consulta: str | None = None
    observaciones: str | None = None
    id_paciente: int | None = None
    id_psicologo: int | None = None
    id_servicio: int | None = None
    id_sala: int | None = None
    id_estado_cita: int | None = None
    recordatorio_enviado: bool | None = None


# ============================================
# MODELOS CLÍNICOS
# ============================================

# Tabla: historial_clinico
class HistorialClinicoBase(SQLModel):
    tipo_registro: str = Field(max_length=50)
    contenido: str
    diagnostico_principal: str | None = Field(default=None, max_length=200)
    diagnostico_secundario: str | None = Field(default=None, max_length=200)
    observaciones: str | None = None
    privado: bool = Field(default=True)


class HistorialClinico(HistorialClinicoBase, table=True):
    __tablename__ = "historial_clinico"

    id_historial: int | None = Field(default=None, primary_key=True)
    id_paciente: int = Field(foreign_key="pacientes.id_paciente")
    id_empleado: int = Field(foreign_key="psicologos.id_empleado")
    fecha_registro: datetime | None = Field(default_factory=datetime.utcnow)

    # Relaciones
    paciente: Paciente = Relationship(back_populates="historiales")
    psicologo: Psicologo = Relationship(back_populates="historiales")


# Tabla: antecedentes_medicos
class AntecedenteMedicoBase(SQLModel):
    tipo_antecedente: str = Field(max_length=50)
    descripcion: str
    fecha_ocurrencia: date | None = None
    relevancia: str | None = Field(default=None, max_length=20)


class AntecedenteMedico(AntecedenteMedicoBase, table=True):
    __tablename__ = "antecedentes_medicos"

    id_antecedente: int | None = Field(default=None, primary_key=True)
    id_paciente: int = Field(foreign_key="pacientes.id_paciente")
    fecha_registro: datetime | None = Field(default_factory=datetime.utcnow)

    # Relaciones
    paciente: Paciente = Relationship(back_populates="antecedentes")


# Tabla: tratamientos
class TratamientoBase(SQLModel):
    tipo_tratamiento: str = Field(max_length=100)
    descripcion: str
    objetivos: str | None = None
    fecha_inicio: date
    fecha_fin_estimada: date | None = None
    fecha_fin_real: date | None = None
    estado: str = Field(default='activo', max_length=30)


class Tratamiento(TratamientoBase, table=True):
    __tablename__ = "tratamientos"

    id_tratamiento: int | None = Field(default=None, primary_key=True)
    id_paciente: int = Field(foreign_key="pacientes.id_paciente")
    id_empleado: int = Field(foreign_key="psicologos.id_empleado")
    id_cita: int | None = Field(default=None, foreign_key="citas.id_cita")
    fecha_registro: datetime | None = Field(default_factory=datetime.utcnow)

    # Relaciones
    paciente: Paciente = Relationship(back_populates="tratamientos")
    psicologo: Psicologo = Relationship(back_populates="tratamientos")
    cita: Optional[Cita] = Relationship(back_populates="tratamientos")
    medicamentos: list["Medicamento"] = Relationship(back_populates="tratamiento")
    seguimientos: list["Seguimiento"] = Relationship(back_populates="tratamiento")


class TratamientoPublic(TratamientoBase):
    id_tratamiento: int
    id_paciente: int
    id_psicologo: int
    id_cita: int | None
    fecha_registro: datetime


class TratamientosPublic(SQLModel):
    data: list[TratamientoPublic]
    count: int


class TratamientoCreate(TratamientoBase):
    id_paciente: int
    id_psicologo: int
    id_cita: int | None = None


class TratamientoUpdate(SQLModel):
    tipo_tratamiento: str | None = Field(default=None, max_length=100)
    descripcion: str | None = None
    objetivos: str | None = None
    fecha_inicio: date | None = None
    fecha_fin_estimada: date | None = None
    fecha_fin_real: date | None = None
    estado: str | None = Field(default=None, max_length=30)


# Tabla: medicamentos
class MedicamentoBase(SQLModel):
    nombre_medicamento: str = Field(max_length=150)
    dosis: str | None = Field(default=None, max_length=100)
    frecuencia: str | None = Field(default=None, max_length=100)
    via_administracion: str | None = Field(default=None, max_length=50)
    fecha_inicio: date
    fecha_fin: date | None = None
    prescrito_por: str | None = Field(default=None, max_length=150)
    observaciones: str | None = None
    estado: str = Field(default='activo', max_length=20)


class Medicamento(MedicamentoBase, table=True):
    __tablename__ = "medicamentos"

    id_medicamento: int | None = Field(default=None, primary_key=True)
    id_paciente: int = Field(foreign_key="pacientes.id_paciente")
    id_tratamiento: int | None = Field(default=None, foreign_key="tratamientos.id_tratamiento")
    fecha_registro: datetime | None = Field(default_factory=datetime.utcnow)

    # Relaciones
    paciente: Paciente = Relationship(back_populates="medicamentos")
    tratamiento: Optional[Tratamiento] = Relationship(back_populates="medicamentos")


class MedicamentoPublic(MedicamentoBase):
    id_medicamento: int
    id_paciente: int
    id_tratamiento: int | None
    fecha_registro: datetime


class MedicamentosPublic(SQLModel):
    data: list[MedicamentoPublic]
    count: int


class MedicamentoCreate(MedicamentoBase):
    id_paciente: int
    id_tratamiento: int | None = None


class MedicamentoUpdate(SQLModel):
    nombre_medicamento: str | None = Field(default=None, max_length=150)
    dosis: str | None = Field(default=None, max_length=100)
    frecuencia: str | None = Field(default=None, max_length=100)
    via_administracion: str | None = Field(default=None, max_length=50)
    fecha_inicio: date | None = None
    fecha_fin: date | None = None
    prescrito_por: str | None = Field(default=None, max_length=150)
    observaciones: str | None = None
    estado: str | None = Field(default=None, max_length=20)


# Tabla: seguimientos
class SeguimientoBase(SQLModel):
    fecha_seguimiento: date
    tipo_seguimiento: str | None = Field(default=None, max_length=50)
    estado_animo: str | None = Field(default=None, max_length=100)
    nivel_funcionalidad: int | None = None
    adherencia_tratamiento: str | None = Field(default=None, max_length=50)
    observaciones: str
    proxima_evaluacion: date | None = None


class Seguimiento(SeguimientoBase, table=True):
    __tablename__ = "seguimientos"

    id_seguimiento: int | None = Field(default=None, primary_key=True)
    id_paciente: int = Field(foreign_key="pacientes.id_paciente")
    id_empleado: int = Field(foreign_key="psicologos.id_empleado")
    id_tratamiento: int | None = Field(default=None, foreign_key="tratamientos.id_tratamiento")
    fecha_registro: datetime | None = Field(default_factory=datetime.utcnow)

    # Relaciones
    paciente: Paciente = Relationship(back_populates="seguimientos")
    psicologo: Psicologo = Relationship(back_populates="seguimientos")
    tratamiento: Optional[Tratamiento] = Relationship(back_populates="seguimientos")


class SeguimientoPublic(SeguimientoBase):
    id_seguimiento: int
    id_paciente: int
    id_psicologo: int
    id_tratamiento: int | None
    fecha_registro: datetime


class SeguimientosPublic(SQLModel):
    data: list[SeguimientoPublic]
    count: int


class SeguimientoCreate(SeguimientoBase):
    id_paciente: int
    id_psicologo: int
    id_tratamiento: int | None = None


class SeguimientoUpdate(SQLModel):
    fecha_seguimiento: date | None = None
    tipo_seguimiento: str | None = Field(default=None, max_length=50)
    estado_animo: str | None = Field(default=None, max_length=100)
    nivel_funcionalidad: int | None = None
    adherencia_tratamiento: str | None = Field(default=None, max_length=50)
    observaciones: str | None = None
    proxima_evaluacion: date | None = None


# Tabla: sesiones_clinicas
class SesionClinicaBase(SQLModel):
    numero_sesion: int | None = None
    duracion_real_minutos: int | None = None
    asistencia: str | None = Field(default=None, max_length=20)
    motivo_ausencia: str | None = None
    notas_sesion: str | None = None
    tecnicas_utilizadas: str | None = None
    tareas_asignadas: str | None = None
    evaluacion_sesion: str | None = None
    proximo_objetivo: str | None = None


class SesionClinica(SesionClinicaBase, table=True):
    __tablename__ = "sesiones_clinicas"

    id_sesion: int | None = Field(default=None, primary_key=True)
    id_cita: int = Field(foreign_key="citas.id_cita")
    id_paciente: int = Field(foreign_key="pacientes.id_paciente")
    id_empleado: int = Field(foreign_key="psicologos.id_empleado")
    fecha_registro: datetime | None = Field(default_factory=datetime.utcnow)

    # Relaciones
    cita: Cita = Relationship(back_populates="sesiones")
    paciente: Paciente = Relationship(back_populates="sesiones")
    psicologo: Psicologo = Relationship(back_populates="sesiones")


# ============================================
# MODELOS DE NOTIFICACIONES
# ============================================

# Tabla: notificaciones
class NotificacionBase(SQLModel):
    email_destinatario: str | None = Field(default=None, max_length=100)
    tipo_notificacion: str = Field(max_length=50)  # confirmacion_inicial, confirmacion_final, cancelacion, reagendamiento, recordatorio
    asunto: str = Field(max_length=200)
    contenido: str
    fecha_programada: datetime | None = None
    estado: str = Field(default='pendiente', max_length=20)  # pendiente, enviada, fallida
    intentos_envio: int = Field(default=0)


class Notificacion(NotificacionBase, table=True):
    __tablename__ = "notificaciones"

    id_notificacion: int | None = Field(default=None, primary_key=True)
    id_cita: int | None = Field(default=None, foreign_key="citas.id_cita")
    id_usuario: int | None = Field(default=None, foreign_key="usuarios.id_usuario")
    fecha_enviada: datetime | None = None
    error_mensaje: str | None = None
    fecha_creacion: datetime | None = Field(default_factory=datetime.utcnow)

    # Relaciones
    usuario: Optional[Usuario] = Relationship(back_populates="notificaciones")
    cita: Optional["Cita"] = Relationship(back_populates="notificaciones")


# ============================================
# SCHEMAS PARA AUTENTICACIÓN (compatibilidad con sistema existente)
# ============================================

class Message(SQLModel):
    message: str


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)
