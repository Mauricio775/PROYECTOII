from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class Inventory(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="MongoDB Id - generado automáticamente"
    )

    id_book: str = Field(
        description="ID del libro asociado",
        examples=["68812f319934647439127302"]
    )

    quantity: int = Field(
        description="Cantidad de libros disponibles",
        examples=[21]
    )

    description: str = Field(
        description="Descripción del inventario",
        examples=["Libros de ciencia ficción"]
    )

    inventory_date: datetime = Field(
        default_factory=datetime.utcnow,
        description="Fecha de creación del inventario"
    )

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: int) -> int:
        if value < 0:
            raise ValueError("La cantidad no puede ser negativa")
        return value

