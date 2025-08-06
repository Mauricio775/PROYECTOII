from  pydantic import BaseModel, Field
from typing import Optional

class Book(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="MongoDB ID - Se genera automáticamente desde el _id de MongoDB, no es necesario enviarlo en POST"
    )

    name: str = Field(
        description="Nombre del libro",
        pattern= r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Juan", "María José"]
    )

    authors: str = Field(
        description="Nombre de Autores",
        pattern= r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Pér", "García López"]
    )

    categories: str = Field(
        description="Categoria segun el gusto de los autores",
        examples=["Ciencia Ficción", "Romanticos"]
    )

    language: str = Field(
        description="lenguaje del libro segun preferencia",
        exameples= ["English","Spanish"]
    )

