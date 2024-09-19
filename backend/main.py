from fastapi import FastAPI
from backend.database.database import get_db
import logging
from backend.database.database import Base, engine
from backend.routers.user import router as user_router
from backend.routers.home import router as home_router
from backend.routers.game import router as game_router
from fastapi.staticfiles import StaticFiles


# Configure logging
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

app = FastAPI()

app.mount("/backend/static", StaticFiles(directory="backend/static"), name="static")

@app.on_event("startup")
def startup():
    # Create the tables in the database
    Base.metadata.create_all(bind=engine)

#Include routers
app.include_router(game_router, prefix="api/games")
app.include_router(home_router)
app.include_router(user_router, prefix="/api/users")