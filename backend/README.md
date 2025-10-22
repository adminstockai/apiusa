# Stock Analysis Landing Page Backend

A complete backend system built with FastAPI, SQLite, and JWT authentication for managing a stock analysis landing page with analytics tracking and admin panel.

## Features

- **FastAPI Backend**: Modern, fast Python web framework
- **SQLite Database**: Lightweight, file-based database
- **JWT Authentication**: Secure admin panel access
- **Analytics Tracking**: Visitor tracking, stock searches, conversion tracking
- **Admin Dashboard**: Real-time statistics and data visualization
- **Settings Management**: Easy configuration of WhatsApp contact links
- **API Compatibility**: Drop-in replacement for existing PHP endpoints

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # SQLite database operations
│   ├── models.py            # Pydantic data models
│   ├── auth.py              # JWT authentication and password hashing
│   └── routers/
│       ├── api.py           # Public API endpoints
│       ├── admin_api.py     # Admin API endpoints
│       └── admin_pages.py   # Admin page routes
├── templates/
│   ├── admin_login.html     # Admin login page
│   ├── admin_dashboard.html # Admin dashboard
│   └── admin_settings.html  # Settings page
├── data/
│   └── app.db              # SQLite database (created on first run)
├── requirements.txt         # Python dependencies
├── init_db.py              # Database initialization script
├── start.sh                # Startup script
├── .env                    # Environment variables
└── README.md               # This file
```

## Installation

**Install Python dependencies**:
```bash
pip install -r requirements.txt
```

## Running the Application

**Simple one-step startup:**
```bash
cd backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

That's it! The application will automatically:
- Create the `data/` directory if it doesn't exist
- Initialize the SQLite database with all required tables
- Create the default admin user (username: adsadmin, password: Mm123567)
- Configure default settings (WhatsApp URL)

The server will start on `http://localhost:8000`

### Optional: Manual Database Initialization

If you want to manually initialize the database before starting the server:
```bash
python3 init_db.py
```

Note: This is optional since the application automatically initializes everything on startup.

## API Endpoints

### Public API (Frontend Compatible)

- `GET /api/token/model/gg-ajax.php` - Returns Google Analytics code
- `GET /api/token/model/cf-ajax.php` - Returns WhatsApp contact link
- `POST /api/analytics/track` - Track analytics events
- `GET /api/analytics/counter` - Get visitor counter
- `POST /api/stock/search` - Log stock code searches

### Admin API (Requires Authentication)

- `POST /admin/api/login` - Admin login (returns JWT token)
- `GET /admin/api/stats` - Get statistics dashboard data
- `GET /admin/api/settings` - Get current settings
- `PUT /admin/api/settings` - Update settings
- `GET /admin/api/visitors` - Get visitor list
- `GET /admin/api/searches` - Get search history
- `GET /admin/api/searches/top` - Get top searched stocks
- `GET /admin/api/events` - Get analytics events

### Admin Pages

- `/admin/login` - Admin login page
- `/admin/dashboard` - Statistics dashboard
- `/admin/settings` - Settings management

### Other Endpoints

- `/` - API information
- `/health` - Health check
- `/docs` - Interactive API documentation (Swagger UI)
- `/redoc` - Alternative API documentation

## Default Admin Credentials

- **Username**: `adsadmin`
- **Password**: `Mm123567`

**Important**: Change these credentials in production by modifying the `.env` file.

## Configuration

Edit the `.env` file to customize:

```env
SECRET_KEY=your-secret-key-change-in-production-min-32-chars-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
DATABASE_PATH=./data/app.db
DEFAULT_ADMIN_USERNAME=adsadmin
DEFAULT_ADMIN_PASSWORD=Mm123567
DEFAULT_WHATSAPP_URL=https://api.whatsapp.com/send/?phone=14433589251&text=Hi
```

## Database Schema

### Tables

1. **admin_users** - Admin user accounts
2. **settings** - System configuration (key-value pairs)
3. **visitors** - Visitor tracking records
4. **stock_searches** - Stock code search logs
5. **analytics_events** - General analytics events

## Usage Examples

### Track a visitor (from frontend):
```javascript
fetch('http://localhost:8000/api/analytics/counter')
  .then(res => res.json())
  .then(data => console.log('Visitors:', data.total_visitors));
```

### Log a stock search:
```javascript
fetch('http://localhost:8000/api/stock/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    stock_code: 'AAPL',
    ip_address: '192.168.1.1',
    user_agent: navigator.userAgent
  })
});
```

### Admin login:
```javascript
fetch('http://localhost:8000/admin/api/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'adsadmin',
    password: 'Mm123567'
  })
})
.then(res => res.json())
.then(data => {
  localStorage.setItem('admin_token', data.access_token);
});
```

### Update WhatsApp URL (authenticated):
```javascript
const token = localStorage.getItem('admin_token');
fetch('http://localhost:8000/admin/api/settings', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    whatsapp_url: 'https://api.whatsapp.com/send/?phone=1234567890&text=Hello'
  })
});
```

## Security Features

- **Password Hashing**: Uses bcrypt for secure password storage
- **JWT Tokens**: Secure, stateless authentication
- **CORS Protection**: Configurable cross-origin resource sharing
- **Input Validation**: Pydantic models validate all inputs
- **SQL Injection Protection**: Parameterized queries throughout

## Development

### Enable debug mode:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

### Access API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Production Deployment

1. Change the `SECRET_KEY` in `.env` to a strong random value
2. Update admin credentials
3. Use a production ASGI server like Gunicorn with Uvicorn workers:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```
4. Set up HTTPS/SSL
5. Configure firewall rules
6. Set up regular database backups

## Troubleshooting

### Database locked error:
- SQLite doesn't handle high concurrency well. Consider using PostgreSQL for production.

### Port already in use:
```bash
# Change port in start.sh or use:
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## License

This project is provided as-is for internal use.
