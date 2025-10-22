#!/usr/bin/env python3
"""
Database Initialization Script

This script manually initializes the database, creates tables, and sets up
the default admin user. However, this is now optional as the FastAPI application
automatically performs all initialization on startup.

Usage:
    python3 init_db.py

Note: You can skip this script and just run uvicorn directly. The application
      will automatically create the database and admin user on first startup.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import db
from app.auth import get_password_hash
from app.config import settings

def initialize_database():
    """Initialize database with tables, admin user, and default settings"""
    print("="*60)
    print("Manual Database Initialization")
    print("="*60)
    print()
    print("Note: This script is optional. The application automatically")
    print("      initializes the database on startup.")
    print()

    try:
        db_dir = os.path.dirname(settings.DATABASE_PATH)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            print(f"✓ Created database directory: {db_dir}")

        db_exists = os.path.exists(settings.DATABASE_PATH)
        if db_exists:
            print(f"⚠ Database already exists at: {settings.DATABASE_PATH}")
            response = input("Do you want to reinitialize? (y/N): ").strip().lower()
            if response != 'y':
                print("Aborted.")
                return

        db.init_database()
        print("✓ Database tables created successfully")

        if not db.admin_user_exists(settings.DEFAULT_ADMIN_USERNAME):
            password_hash = get_password_hash(settings.DEFAULT_ADMIN_PASSWORD)
            db.create_admin_user(settings.DEFAULT_ADMIN_USERNAME, password_hash)
            print(f"✓ Admin user created: {settings.DEFAULT_ADMIN_USERNAME}")
        else:
            print(f"✓ Admin user already exists: {settings.DEFAULT_ADMIN_USERNAME}")

        db.set_setting('whatsapp_url', settings.DEFAULT_WHATSAPP_URL)
        print(f"✓ Default WhatsApp URL configured")

        print()
        print("="*60)
        print("✅ Database Initialization Complete!")
        print("="*60)
        print(f"Database: {settings.DATABASE_PATH}")
        print(f"Admin username: {settings.DEFAULT_ADMIN_USERNAME}")
        print(f"Admin password: {settings.DEFAULT_ADMIN_PASSWORD}")
        print()
        print("Start the server with:")
        print("  cd backend")
        print("  python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
        print("="*60)

    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    initialize_database()
