from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.config import settings

router = APIRouter()
templates = Jinja2Templates(directory=settings.TEMPLATE_DIR)

@router.get("/admin", response_class=HTMLResponse)
async def get_admin_panel(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})