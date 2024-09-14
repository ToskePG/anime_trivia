from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse

# Initialize APIRouter
router = APIRouter()

# Set up Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

# Home route to render the home page
@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Serve favicon from static/images folder
@router.get("/favicon.png", include_in_schema=False)
async def favicon():
    return FileResponse("static/images/favicon.png")