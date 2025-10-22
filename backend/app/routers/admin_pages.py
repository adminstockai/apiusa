from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="templates")

@router.get("/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard_page(request: Request):
    return templates.TemplateResponse("admin_dashboard.html", {"request": request})

@router.get("/settings", response_class=HTMLResponse)
async def admin_settings_page(request: Request):
    return templates.TemplateResponse("admin_settings.html", {"request": request})

@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
async def admin_root(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})
