from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Order(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="MongoDB Id- Id generado automaticamente en MongoDB"
    )
    
    id_user: str = Field(
        description= "ID del usuario que realizo la orden",
        examples=["68812f319934647439127302"]
    )
    
    order_date: datetime = Field(
        default_factory=datetime.utcnow,
        description= "Fecha de creación de la orden"
    )
    
    subtotal: float = Field(
        description= "Subtotal de la orden",
        gt=0,
        example=[222.8,290.3]
    )
    
    taxes: float = Field(
        description= "Impuesto de la orden",
        ge=0,
        example=[12.8,2.9]
    )
    
    discount: float = Field(
        default=0.0,
        description= "Descuento de la ordem",
        ge=0,
        example=[0.21,29.0]
    )
    
    total: float = Field(
        description= "Total de la orden",
        gt=0,
        examples=[344.23, 103.88]
    )

    