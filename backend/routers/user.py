from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.database.database import get_db
from backend.database.models import User
from backend.schemas.schemas import UserResponse

router = APIRouter()

@router.get("/", response_model=List[UserResponse], tags=['User'])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


