from pydantic import BaseModel, Field
from typing import Optional


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    price: float = Field(..., gt=0)
    quantity: int = Field(default=1, ge=1)
    description: Optional[str] = None


class ItemResponse(ItemCreate):
    id: int

    class Config:
        orm_mode = True
