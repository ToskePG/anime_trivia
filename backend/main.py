from fastapi import FastAPI
from backend.database.database import get_db
import logging
from backend.database.database import Base, engine


# Configure logging
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

app = FastAPI()

@app.on_event("startup")
def startup():
    # Create the tables in the database
    Base.metadata.create_all(bind=engine)