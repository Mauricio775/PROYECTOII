from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class PaymentsType(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="MongoDB Id - generado automáticamente"
    )

    id_payments: str = Field(
        description="ID del libro asociado",
        examples=["68854ead23ca0ae72d325c73"]
    )

    state_method: str = Field(
        description= "Estado de Pago",
        examples= ["Pendiente", "En proceso", "Pagado", "Cancelado", "En revision" ]
    )
    