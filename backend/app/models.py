from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AdminLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class SettingsUpdate(BaseModel):
    whatsapp_url: str

class SettingsResponse(BaseModel):
    whatsapp_url: str
    updated_at: Optional[str] = None

class VisitorCreate(BaseModel):
    ip_address: str
    user_agent: Optional[str] = None
    referer: Optional[str] = None

class StockSearchCreate(BaseModel):
    stock_code: str
    ip_address: str
    user_agent: Optional[str] = None

class AnalyticsEvent(BaseModel):
    event_type: str
    ip_address: str
    stock_code: Optional[str] = None
    metadata: Optional[str] = None

class StatsResponse(BaseModel):
    total_visitors: int
    today_visitors: int
    total_searches: int
    today_searches: int
    total_conversions: int
    today_conversions: int
    conversion_rate: float
