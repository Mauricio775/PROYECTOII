from  pydantic import BaseModel, Field
from typing import Optional

class Book(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="MongoDB ID - Se genera automáticamente desde el _id de MongoDB, no es necesario enviarlo en POST"
    )

    description: str = Field(
        description="Nombre del libro",
        pattern= r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Juan", "María José"]
    )
   ########Agregado 
    active: bool = Field(
        default= True,
        description= "Estado Activo del libro"
    )

