from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from app.api.deps import SessionDep
from app.core.security import get_password_hash
from app.models import (
    Usuario,
    UsuarioPublic,
)

router = APIRouter(tags=["private"], prefix="/private")


class PrivateUserCreate(BaseModel):
    nombre_usuario: str
    email: str
    password: str


@router.post("/users/", response_model=UsuarioPublic)
def create_user(user_in: PrivateUserCreate, session: SessionDep) -> Any:
    """
    Create a new user.
    """

    user = Usuario(
        nombre_usuario=user_in.nombre_usuario,
        email=user_in.email,
        contrasena=get_password_hash(user_in.password),
    )

    session.add(user)
    session.commit()

    return user
