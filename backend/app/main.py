from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
from app.routers import api, admin_api, admin_pages
from app.database import db

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

static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.on_event("startup")
async def startup_event():
    db.init_database()
    print("Database initialized successfully")

@app.get("/")
async def root():
    return {
        "message": "Stock Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "api_docs": "/docs",
            "admin_panel": "/admin",
            "health_check": "/health"
        }
    }

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
