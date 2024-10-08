from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    is_confirmed: bool

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class GameCreate(BaseModel):
    player1_id: int
    player2_id: int

class GameResponse(BaseModel):
    id: int
    player1_id: int
    player2_id: int

    class Config:
        from_attributes = True