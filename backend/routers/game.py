from backend.database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.models import Game
from backend.schemas.schemas import GameCreate, GameResponse

router = APIRouter()

@router.get('/', response_model=list[GameResponse], tags=['Game'])
def list_all_games(db: Session = Depends(get_db)):
    games = db.query(Game).all()
    return games