from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class Payment(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="MongoDB Id - generado automáticamente"
    )
    
    id_order: Optional[str] = Field(
        default=None,
        description="ID de la orden asociada (si aplica)",
        example="70f2c9c298be4df5e1bc34d9"
    )
    
    amount: float = Field(
        description="Monto pagado",
        gt=0,
        example= 1250.75
        
    )
    
    state_method: str = Field(
        description= "Estado de Pago",
        examples= ["Pendiente", "En proceso", "Pagado", "Cancelado", "En revision" ]
    )
    
    payment_date: datetime = Field(
        default_factory=datetime.utcnow,
        description="Fecha de creación del inventario"
    )
    
    @field_validator("state_method")
    @classmethod
    def validate_state(cls, value):
        estados_validos = ["Pendiente", "En proceso", "Pagado", "Cancelado", "En revisión"]
        if value not in estados_validos:
            raise ValueError(f"Estado inválido. Debe ser uno de: {', '.join(estados_validos)}")
        return value


