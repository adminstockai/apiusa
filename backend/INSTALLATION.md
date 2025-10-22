# Installation Guide

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Or if using pip3:
```bash
pip3 install -r requirements.txt
```

### 2. Initialize Database

```bash
python init_db.py
```

Or with python3:
```bash
python3 init_db.py
```

This will create:
- SQLite database at `data/app.db`
- Admin user with username: `adsadmin` and password: `Mm123567`
- Default WhatsApp URL configuration

### 3. Start the Server

**Option A: Using the startup script**
```bash
sh start.sh
```

**Option B: Direct uvicorn command**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Or with python3:
```bash
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Access the Application

- **Frontend API**: http://localhost:8000/api/
- **Admin Login**: http://localhost:8000/admin/login
- **Admin Dashboard**: http://localhost:8000/admin/dashboard
- **API Documentation**: http://localhost:8000/docs

## Default Credentials

- **Username**: `adsadmin`
- **Password**: `Mm123567`

**IMPORTANT**: Change these in the `.env` file for production use!

## Dependencies

The following packages will be installed:

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-jose` - JWT token handling
- `passlib` - Password hashing
- `python-multipart` - Form data parsing
- `pydantic` - Data validation
- `pydantic-settings` - Settings management
- `python-dotenv` - Environment variables
- `jinja2` - Template engine
- `aiosqlite` - Async SQLite driver

## Troubleshooting

### pip not found
If you get "pip not found", try:
```bash
python3 -m pip install -r requirements.txt
```

### Permission denied on start.sh
```bash
chmod +x start.sh
```

### Port 8000 already in use
Change the port in the uvicorn command:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### Module not found errors
Make sure you're in the backend directory and all dependencies are installed:
```bash
cd backend
pip install -r requirements.txt
```

## Manual Installation Steps

If the automated script doesn't work, follow these steps:

1. **Install dependencies**:
```bash
pip install fastapi==0.109.0
pip install uvicorn[standard]==0.27.0
pip install python-jose[cryptography]==3.3.0
pip install passlib[bcrypt]==1.7.4
pip install python-multipart==0.0.6
pip install pydantic==2.5.3
pip install pydantic-settings==2.1.0
pip install python-dotenv==1.0.0
pip install jinja2==3.1.3
pip install aiosqlite==0.19.0
```

2. **Create data directory**:
```bash
mkdir -p data
```

3. **Run initialization**:
```bash
python init_db.py
```

4. **Start server**:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Verifying Installation

Once the server is running, you should see output like:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
Database initialized successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Visit http://localhost:8000/health to verify the API is working.

## Next Steps

1. Login to the admin panel at http://localhost:8000/admin/login
2. Configure your WhatsApp URL in the settings
3. Test the API endpoints using the documentation at http://localhost:8000/docs
4. Integrate the frontend with the new backend API endpoints
