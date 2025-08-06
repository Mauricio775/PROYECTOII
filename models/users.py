from  pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class User(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="MongoDB ID - Se genera automaticamente en mongodb"
    )

    name: str = Field(
        description="Primer Nombre",
        pattern= r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Angel", "Valladares"]
    )

    lastname: str = Field(
        description="Apellidos",
        pattern= r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Valladares", "Oseguera"]
    )

    email: str = Field(
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        examples=["mauricio@proyecto.com"]
    )

    active: bool = Field(
        default=True,
        description="Estado activo del usuario"
    )

    admin: bool = Field(
        default=False,
        description="Permisos de administrador"
    )

    password: str = Field(
        min_length=8,
        max_length=64,
        description="Contraseña del usuario, debe tener entre 8 y 64 caracteres incluir por lo menos un numero, por lo menos una mayuscula y por lo menos un caracter especial.",
        examples=["Aeropuerto@2025"]
    )

    @field_validator('password')
    @classmethod
    def validate_password_complexity(cls, value: str):
        if not re.search(r"[A-Z]", value):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r"\d", value):
            raise ValueError("La contraseña debe contener al menos un número.")
        if not re.search(r"[@$!%*?&]", value):
            raise ValueError("La contraseña debe contener al menos un carácter especial (@$!%*?&).")
        return value