from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# For creating a new user
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

# For responses
class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    price: float = Field(..., gt=0)
    quantity: int = Field(default=1, ge=1)
    description: Optional[str] = None


class ItemResponse(ItemCreate):
    id: int

    class Config:
        orm_mode = True
