import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import db
from app.auth import get_password_hash
from app.config import settings

def initialize_database():
    print("Initializing database...")

    db.init_database()
    print("Database tables created successfully")

    password_hash = get_password_hash(settings.DEFAULT_ADMIN_PASSWORD)
    db.create_admin_user(settings.DEFAULT_ADMIN_USERNAME, password_hash)
    print(f"Admin user created: {settings.DEFAULT_ADMIN_USERNAME}")

    db.set_setting('whatsapp_url', settings.DEFAULT_WHATSAPP_URL)
    print(f"Default WhatsApp URL set: {settings.DEFAULT_WHATSAPP_URL}")

    print("\nDatabase initialization complete!")
    print(f"Admin username: {settings.DEFAULT_ADMIN_USERNAME}")
    print(f"Admin password: {settings.DEFAULT_ADMIN_PASSWORD}")
    print("\nYou can now start the server with: sh start.sh")

if __name__ == "__main__":
    initialize_database()
