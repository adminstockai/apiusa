import sqlite3
import aiosqlite
from datetime import datetime
from typing import List, Dict, Optional, Any
from app.config import settings
import os

class Database:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or settings.DATABASE_PATH
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            print(f"Created database directory: {db_dir}")

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    async def get_async_connection(self):
        conn = await aiosqlite.connect(self.db_path)
        conn.row_factory = aiosqlite.Row
        return conn

    def init_database(self):
        print(f"Initializing database at: {self.db_path}")
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS visitors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT NOT NULL,
                user_agent TEXT,
                referer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_visitors_ip ON visitors(ip_address)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_visitors_created ON visitors(created_at)
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_code TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_searches_stock ON stock_searches(stock_code)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_searches_created ON stock_searches(created_at)
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                stock_code TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_events_type ON analytics_events(event_type)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_events_created ON analytics_events(created_at)
        ''')

        conn.commit()
        conn.close()
        print("Database tables created successfully")

    def create_admin_user(self, username: str, password_hash: str) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT OR IGNORE INTO admin_users (username, password_hash) VALUES (?, ?)',
                (username, password_hash)
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def admin_user_exists(self, username: str) -> bool:
        """Check if admin user exists"""
        user = self.get_admin_user(username)
        return user is not None

    def get_admin_user(self, username: str) -> Optional[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM admin_users WHERE username = ?', (username,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def set_setting(self, key: str, value: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''INSERT INTO settings (key, value, updated_at)
                   VALUES (?, ?, CURRENT_TIMESTAMP)
                   ON CONFLICT(key) DO UPDATE SET value = ?, updated_at = CURRENT_TIMESTAMP''',
                (key, value, value)
            )
            conn.commit()
        finally:
            conn.close()

    def get_setting(self, key: str) -> Optional[str]:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
            row = cursor.fetchone()
            return row['value'] if row else None
        finally:
            conn.close()

    def get_all_settings(self) -> Dict[str, str]:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT key, value FROM settings')
            rows = cursor.fetchall()
            return {row['key']: row['value'] for row in rows}
        finally:
            conn.close()

    def add_visitor(self, ip_address: str, user_agent: str = None, referer: str = None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO visitors (ip_address, user_agent, referer) VALUES (?, ?, ?)',
                (ip_address, user_agent, referer)
            )
            conn.commit()
        finally:
            conn.close()

    def add_stock_search(self, stock_code: str, ip_address: str, user_agent: str = None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO stock_searches (stock_code, ip_address, user_agent) VALUES (?, ?, ?)',
                (stock_code, ip_address, user_agent)
            )
            conn.commit()
        finally:
            conn.close()

    def add_analytics_event(self, event_type: str, ip_address: str, stock_code: str = None, metadata: str = None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO analytics_events (event_type, ip_address, stock_code, metadata) VALUES (?, ?, ?, ?)',
                (event_type, ip_address, stock_code, metadata)
            )
            conn.commit()
        finally:
            conn.close()

    def get_stats(self) -> Dict[str, Any]:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT COUNT(DISTINCT ip_address) as total FROM visitors')
            total_visitors = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(DISTINCT ip_address) as today FROM visitors WHERE DATE(created_at) = DATE('now')")
            today_visitors = cursor.fetchone()['today']

            cursor.execute('SELECT COUNT(*) as total FROM stock_searches')
            total_searches = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) as today FROM stock_searches WHERE DATE(created_at) = DATE('now')")
            today_searches = cursor.fetchone()['today']

            cursor.execute("SELECT COUNT(*) as total FROM analytics_events WHERE event_type = 'whatsapp_click'")
            total_conversions = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) as today FROM analytics_events WHERE event_type = 'whatsapp_click' AND DATE(created_at) = DATE('now')")
            today_conversions = cursor.fetchone()['today']

            conversion_rate = (total_conversions / total_visitors * 100) if total_visitors > 0 else 0

            return {
                'total_visitors': total_visitors,
                'today_visitors': today_visitors,
                'total_searches': total_searches,
                'today_searches': today_searches,
                'total_conversions': total_conversions,
                'today_conversions': today_conversions,
                'conversion_rate': round(conversion_rate, 2)
            }
        finally:
            conn.close()

    def get_visitors(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'SELECT * FROM visitors ORDER BY created_at DESC LIMIT ? OFFSET ?',
                (limit, offset)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def get_searches(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'SELECT * FROM stock_searches ORDER BY created_at DESC LIMIT ? OFFSET ?',
                (limit, offset)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def get_top_searches(self, limit: int = 10) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''SELECT stock_code, COUNT(*) as count
                   FROM stock_searches
                   GROUP BY stock_code
                   ORDER BY count DESC
                   LIMIT ?''',
                (limit,)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def get_events(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'SELECT * FROM analytics_events ORDER BY created_at DESC LIMIT ? OFFSET ?',
                (limit, offset)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

db = Database()
