from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
import os
from app.routers import api, admin_api, admin_pages
from app.database import db
from app.auth import get_password_hash
from app.config import settings

app = FastAPI(
    title="Stock Analysis Landing Page API",
    description="Backend API for stock analysis landing page with admin panel",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router)
app.include_router(admin_api.router)
app.include_router(admin_pages.router)

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
root_static_path = os.path.join(project_root, "static")
if os.path.exists(root_static_path):
    app.mount("/static", StaticFiles(directory=root_static_path), name="static")

model_path = os.path.join(project_root, "model")
if os.path.exists(model_path):
    app.mount("/model", StaticFiles(directory=model_path), name="model")

@app.on_event("startup")
async def startup_event():
    """
    Automatic initialization on startup:
    - Creates database directory if not exists
    - Initializes database tables
    - Creates default admin user
    - Configures default settings
    """
    print("="*60)
    print("Stock Analysis Landing Page Backend Starting...")
    print("="*60)
    print()

    try:
        db_dir = os.path.dirname(settings.DATABASE_PATH)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            print(f"✓ Created database directory: {db_dir}")

        db_exists = os.path.exists(settings.DATABASE_PATH)
        if not db_exists:
            print(f"✓ Creating new database: {settings.DATABASE_PATH}")

        db.init_database()

        if not db_exists:
            print("✓ Database tables created successfully")

        if not db.admin_user_exists(settings.DEFAULT_ADMIN_USERNAME):
            print(f"✓ Creating default admin user: {settings.DEFAULT_ADMIN_USERNAME}")
            password_hash = get_password_hash(settings.DEFAULT_ADMIN_PASSWORD)
            created = db.create_admin_user(settings.DEFAULT_ADMIN_USERNAME, password_hash)
            if created:
                print(f"✓ Admin user '{settings.DEFAULT_ADMIN_USERNAME}' created successfully")
        else:
            print(f"✓ Admin user '{settings.DEFAULT_ADMIN_USERNAME}' verified")

        whatsapp_url = db.get_setting('whatsapp_url')
        if not whatsapp_url:
            db.set_setting('whatsapp_url', settings.DEFAULT_WHATSAPP_URL)
            print(f"✓ Default WhatsApp URL configured")
        else:
            print(f"✓ WhatsApp URL configured")

        print()
        print("="*60)
        print("✅ Backend Ready!")
        print("="*60)
        print(f"🌐 Main Page:    http://127.0.0.1:8000/")
        print(f"🔐 Admin Panel:  http://127.0.0.1:8000/admin")
        print(f"📚 API Docs:     http://127.0.0.1:8000/docs")
        print(f"❤️  Health Check: http://127.0.0.1:8000/health")
        print()
        print(f"Default Admin Credentials:")
        print(f"  Username: {settings.DEFAULT_ADMIN_USERNAME}")
        print(f"  Password: {settings.DEFAULT_ADMIN_PASSWORD}")
        print("="*60)

    except Exception as e:
        print(f"❌ Error during startup: {e}")
        import traceback
        traceback.print_exc()
        raise

@app.get("/")
async def root():
    index_path = os.path.join(project_root, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "message": "Stock Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "api_docs": "/docs",
            "admin_panel": "/admin",
            "health_check": "/health"
        }
    }

@app.get("/disclaimer.html")
async def disclaimer():
    return FileResponse(os.path.join(project_root, "disclaimer.html"))

@app.get("/terms.html")
async def terms():
    return FileResponse(os.path.join(project_root, "terms.html"))

@app.get("/privacy.html")
async def privacy():
    return FileResponse(os.path.join(project_root, "privacy.html"))

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc)
        }
    )
