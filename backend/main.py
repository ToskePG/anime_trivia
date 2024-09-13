from fastapi import FastAPI
from backend.database.database import init_db
import logging

# Configure logging
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

app = FastAPI()

# Initialize database
init_db()

@app.get("/")
def check_health():
    return {
        "message": "Healthy",
        "statis": "200 OK"
    }