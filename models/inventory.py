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

    name: str = Field(
        description="Nombre del Inventario",
        examples=["Inventario de Libros"]
    )

    description: str = Field(
        description="Descripción del inventario",
        examples=["Libros de ciencia ficción"]
    )
    
    cost: float = Field(
        description="Costo del Inventario",
        gt=0,
        examples=[150.50, 89.99]
    )

    discount: int = Field(
        description="Descuento en porcentaje (0-100)",
        ge=0,
        le=100,
        default=0,
        examples=[10, 25, 0]
    )

    active: bool = Field(
        default=True,
        description="Estado activo del Inventario"
    )

