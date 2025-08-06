from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class State(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="MongoDB Id - generado automáticamente"
    )
    
    description: str = Field(
        description="Descripción del Pago",
        examples=["Pendiente", "En proceso", "Pagado", "Cancelado", "En Revision"]
    )
    
    
class CreateState(BaseModel):
    description: str = Field(
        description="Descripción del estado del pago",
        examples=["Pendiente", "En proceso", "Pagado", "Cancelado", "En Revision"]
    )