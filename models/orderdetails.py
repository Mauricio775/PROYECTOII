from pydantic import BaseModel, Field, field_validator
from typing import Optional

class OrderDetails(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="MongoDB Id - generado automáticamente"
    )

    id_inventory: str = Field(
        description="ID del libro asociado",
        examples=["68854ead23ca0ae72d325c73"]
    )

    id_order: str = Field(
        description="ID de la orden asociada",
        examples=["68812f319934647439127302"]
    )
    
    quantity: int = Field(
        description="Cantidad de libros ordenes",
        examples=[12]
    )
