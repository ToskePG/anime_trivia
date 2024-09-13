from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class GameCreate(BaseModel):
    player1_id: int
    player2_id: int

class GameResponse(BaseModel):
    id: int
    player1_id: int
    player2_id: int

    class Config:
        orm_mode = True