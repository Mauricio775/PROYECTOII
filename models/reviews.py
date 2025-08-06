from  pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class Review(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="MongoDB Id- Id generado automaticamente en MongoDB"
        
    )
    
    id_user: str = Field(
        description= "ID del usuario que realizo la reseña",
        examples=["68812f319934647439127302"]
    )
    
    id_book: str = Field(
        description= "ID del libro del cual se realizo la reseña",
        examples=["6882c9c298be4df5e1ba92c6"]
    )
    
    review_date: datetime = Field(
        default_factory=datetime.utcnow,
        description= "Fecha de creación de la reseña"
        
    )
    
    rating: float = Field(
        description= "Calificacion de la reseña del 1-10 en decimales se puede",
        example=[8.8,2.3]
    )
    
    comment: str = Field(
        description= "Comentario sobre el libro",
        example= ["Excelente libro"]
    )
    
    @field_validator("rating")
    @classmethod
    def validate_rating(cls, value:float):
        if not (1.0 <= value <= 10.0):
            raise ValueError("La calificacion debe estar entre 1.0 y 10.0")
        return value 
    
    
    @field_validator("comment")
    @classmethod
    def validate_comment(cls, value:str):
        if not value.strip():
            raise ValueError("El comentario no debe de estar vacio")
        return value
    
    
    
    
    