from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
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

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
root_static_path = os.path.join(project_root, "static")
if os.path.exists(root_static_path):
    app.mount("/static", StaticFiles(directory=root_static_path), name="static")

model_path = os.path.join(project_root, "model")
if os.path.exists(model_path):
    app.mount("/model", StaticFiles(directory=model_path), name="model")

@app.on_event("startup")
async def startup_event():
    db.init_database()
    print("Database initialized successfully")

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
