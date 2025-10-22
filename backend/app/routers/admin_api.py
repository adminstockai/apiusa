from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from app.database import db
from app.auth import verify_password, create_access_token, get_current_user
from app.models import AdminLogin, Token, SettingsUpdate, SettingsResponse, StatsResponse
from app.config import settings

router = APIRouter(prefix="/admin/api")

@router.post("/login", response_model=Token)
async def login(credentials: AdminLogin):
    user = db.get_admin_user(credentials.username)

    if not user or not verify_password(credentials.password, user['password_hash']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/stats", response_model=StatsResponse)
async def get_statistics(current_user: str = Depends(get_current_user)):
    stats = db.get_stats()
    return stats

@router.get("/settings", response_model=SettingsResponse)
async def get_settings(current_user: str = Depends(get_current_user)):
    whatsapp_url = db.get_setting('whatsapp_url')
    if not whatsapp_url:
        whatsapp_url = settings.DEFAULT_WHATSAPP_URL

    return {
        "whatsapp_url": whatsapp_url,
        "updated_at": None
    }

@router.put("/settings")
async def update_settings(
    settings_update: SettingsUpdate,
    current_user: str = Depends(get_current_user)
):
    db.set_setting('whatsapp_url', settings_update.whatsapp_url)
    return {
        "status": "success",
        "message": "WhatsApp URL updated successfully",
        "whatsapp_url": settings_update.whatsapp_url
    }

@router.get("/visitors")
async def get_visitors(
    limit: int = 100,
    offset: int = 0,
    current_user: str = Depends(get_current_user)
):
    visitors = db.get_visitors(limit, offset)
    return {"visitors": visitors, "count": len(visitors)}

@router.get("/searches")
async def get_searches(
    limit: int = 100,
    offset: int = 0,
    current_user: str = Depends(get_current_user)
):
    searches = db.get_searches(limit, offset)
    return {"searches": searches, "count": len(searches)}

@router.get("/searches/top")
async def get_top_searches(
    limit: int = 10,
    current_user: str = Depends(get_current_user)
):
    top_searches = db.get_top_searches(limit)
    return {"top_searches": top_searches}

@router.get("/events")
async def get_events(
    limit: int = 100,
    offset: int = 0,
    current_user: str = Depends(get_current_user)
):
    events = db.get_events(limit, offset)
    return {"events": events, "count": len(events)}
