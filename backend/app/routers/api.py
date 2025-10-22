from fastapi import APIRouter, Request, Response
from app.database import db
from app.models import StockSearchCreate, AnalyticsEvent

router = APIRouter()

@router.get("/api/token/model/gg-ajax.php")
async def get_google_analytics():
    ga_code = """
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=UA-XXXXXXXXX-X"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'UA-XXXXXXXXX-X');
    </script>
    """
    return {"pixel": ga_code}

@router.get("/api/token/model/cf-ajax.php")
async def get_whatsapp_link(request: Request):
    whatsapp_url = db.get_setting('whatsapp_url')
    if not whatsapp_url:
        from app.config import settings
        whatsapp_url = settings.DEFAULT_WHATSAPP_URL
        db.set_setting('whatsapp_url', whatsapp_url)

    client_ip = request.client.host if request.client else "unknown"
    db.add_analytics_event('whatsapp_view', client_ip)

    return Response(content=whatsapp_url, media_type="text/plain")

@router.post("/api/analytics/track")
async def track_event(event: AnalyticsEvent):
    db.add_analytics_event(
        event_type=event.event_type,
        ip_address=event.ip_address,
        stock_code=event.stock_code,
        metadata=event.metadata
    )
    return {"status": "success"}

@router.get("/api/analytics/counter")
async def get_visitor_counter(request: Request):
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "")
    referer = request.headers.get("referer", "")

    db.add_visitor(client_ip, user_agent, referer)

    stats = db.get_stats()
    return {
        "total_visitors": stats['total_visitors'],
        "today_visitors": stats['today_visitors'],
        "online_now": stats['today_visitors']
    }

@router.post("/api/stock/search")
async def log_stock_search(search: StockSearchCreate):
    db.add_stock_search(
        stock_code=search.stock_code,
        ip_address=search.ip_address,
        user_agent=search.user_agent
    )
    return {"status": "success", "stock_code": search.stock_code}
