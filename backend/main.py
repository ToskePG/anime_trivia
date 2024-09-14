from fastapi import FastAPI, Depends, HTTPException
from backend.database.database import init_db, get_db
from sqlalchemy import Session
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

# Health check endpoint to test database connection
@app.get("/db_connection")
def check_db_connection(db: Session = Depends(get_db)):
    try:
        # Execute a simple query to check the connection
        db.execute("SELECT 1")
        return {"status": "Database connection successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection failed")