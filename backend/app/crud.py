from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import Usuario, UsuarioCreate, UsuarioUpdate


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
