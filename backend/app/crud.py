from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import (
    Usuario, UsuarioCreate, UsuarioUpdate,
    Paciente, PacienteCreate, PacienteUpdate,
    Cita, CitaCreate, CitaUpdate,
    Tratamiento, TratamientoCreate, TratamientoUpdate,
    Medicamento, MedicamentoCreate, MedicamentoUpdate,
    Seguimiento, SeguimientoCreate, SeguimientoUpdate,
    SalaAtencion, SalaAtencionCreate, SalaAtencionUpdate,
)


def create_user(*, session: Session, user_create: UsuarioCreate) -> Usuario:
    """Crear un nuevo usuario en el sistema"""
    db_obj = Usuario.model_validate(
        user_create, update={"contrasena": get_password_hash(user_create.contrasena)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: Usuario, user_in: UsuarioUpdate) -> Any:
    """Actualizar información de un usuario existente"""
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "contrasena" in user_data:
        password = user_data["contrasena"]
        hashed_password = get_password_hash(password)
        extra_data["contrasena"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> Usuario | None:
    """Obtener usuario por email"""
    statement = select(Usuario).where(Usuario.email == email)
    session_user = session.exec(statement).first()
    return session_user


def get_user_by_username(*, session: Session, nombre_usuario: str) -> Usuario | None:
    """Obtener usuario por nombre de usuario"""
    statement = select(Usuario).where(Usuario.nombre_usuario == nombre_usuario)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> Usuario | None:
    """Autenticar usuario con email y contraseña"""
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.contrasena):
        return None
    return db_user


# ============================================
# CRUD PACIENTES
# ============================================

def create_paciente(*, session: Session, paciente_create: PacienteCreate) -> Paciente:
    """Crear un nuevo paciente en el sistema"""
    db_obj = Paciente.model_validate(paciente_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_paciente(*, session: Session, db_paciente: Paciente, paciente_in: PacienteUpdate) -> Any:
    """Actualizar información de un paciente existente"""
    paciente_data = paciente_in.model_dump(exclude_unset=True)
    db_paciente.sqlmodel_update(paciente_data)
    session.add(db_paciente)
    session.commit()
    session.refresh(db_paciente)
    return db_paciente


def get_paciente_by_rut(*, session: Session, rut: str) -> Paciente | None:
    """Obtener paciente por RUT"""
    statement = select(Paciente).where(Paciente.rut == rut)
    paciente = session.exec(statement).first()
    return paciente


# ============================================
# CRUD CITAS
# ============================================

def create_cita(*, session: Session, cita_create: CitaCreate) -> Cita:
    """Crear una nueva cita en el sistema"""
    db_obj = Cita.model_validate(cita_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_cita(*, session: Session, db_cita: Cita, cita_in: CitaUpdate) -> Any:
    """Actualizar información de una cita existente"""
    cita_data = cita_in.model_dump(exclude_unset=True)
    db_cita.sqlmodel_update(cita_data)
    session.add(db_cita)
    session.commit()
    session.refresh(db_cita)
    return db_cita


# ============================================
# CRUD TRATAMIENTOS
# ============================================

def create_tratamiento(*, session: Session, tratamiento_create: TratamientoCreate) -> Tratamiento:
    """Crear un nuevo tratamiento en el sistema"""
    db_obj = Tratamiento.model_validate(tratamiento_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_tratamiento(*, session: Session, db_tratamiento: Tratamiento, tratamiento_in: TratamientoUpdate) -> Any:
    """Actualizar información de un tratamiento existente"""
    tratamiento_data = tratamiento_in.model_dump(exclude_unset=True)
    db_tratamiento.sqlmodel_update(tratamiento_data)
    session.add(db_tratamiento)
    session.commit()
    session.refresh(db_tratamiento)
    return db_tratamiento


# ============================================
# CRUD MEDICAMENTOS
# ============================================

def create_medicamento(*, session: Session, medicamento_create: MedicamentoCreate) -> Medicamento:
    """Crear un nuevo medicamento en el sistema"""
    db_obj = Medicamento.model_validate(medicamento_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_medicamento(*, session: Session, db_medicamento: Medicamento, medicamento_in: MedicamentoUpdate) -> Any:
    """Actualizar información de un medicamento existente"""
    medicamento_data = medicamento_in.model_dump(exclude_unset=True)
    db_medicamento.sqlmodel_update(medicamento_data)
    session.add(db_medicamento)
    session.commit()
    session.refresh(db_medicamento)
    return db_medicamento


# ============================================
# CRUD SEGUIMIENTOS
# ============================================

def create_seguimiento(*, session: Session, seguimiento_create: SeguimientoCreate) -> Seguimiento:
    """Crear un nuevo seguimiento en el sistema"""
    db_obj = Seguimiento.model_validate(seguimiento_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_seguimiento(*, session: Session, db_seguimiento: Seguimiento, seguimiento_in: SeguimientoUpdate) -> Any:
    """Actualizar información de un seguimiento existente"""
    seguimiento_data = seguimiento_in.model_dump(exclude_unset=True)
    db_seguimiento.sqlmodel_update(seguimiento_data)
    session.add(db_seguimiento)
    session.commit()
    session.refresh(db_seguimiento)
    return db_seguimiento


# ============================================
# CRUD SALAS DE ATENCION
# ============================================

def create_sala_atencion(*, session: Session, sala_create: SalaAtencionCreate) -> SalaAtencion:
    """Crear una nueva sala de atención en el sistema"""
    db_obj = SalaAtencion.model_validate(sala_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_sala_atencion(*, session: Session, db_sala: SalaAtencion, sala_in: SalaAtencionUpdate) -> Any:
    """Actualizar información de una sala de atención existente"""
    sala_data = sala_in.model_dump(exclude_unset=True)
    db_sala.sqlmodel_update(sala_data)
    session.add(db_sala)
    session.commit()
    session.refresh(db_sala)
    return db_sala
