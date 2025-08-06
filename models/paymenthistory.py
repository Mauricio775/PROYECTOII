from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class PaymentHistory(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="MongoDB Id - generado automáticamente"
    )

    id_payments: str = Field(
        description="ID del pago asociado",
        examples=["68854ead23ca0ae72d325c73"]
    )

    id_state: str = Field(
        description="ID del estado asociado al pago",
        examples=["68812f319934647439127302"]
    )
    
    id_payments_type: str = Field(
        description="ID del type payments",
        examples=["68812f319934647439127302"]
    )
    
    quantity: int = Field(
        description="Cantidad de libros ordenes",
        examples=[12]
    )