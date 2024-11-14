import sqlite3
from datetime import datetime, timedelta
from config.settings import Config


class Database:
    def __init__(self):
        self.db_path = Config.DATABASE
        self.init_db()

    def get_db_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        return conn

    def init_db(self):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS urls (
                    original_url TEXT PRIMARY KEY,  -- Already creates an index
                    short_code TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL
                )
                """
            )
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_short_code ON urls 
                (short_code, expires_at)
                """
            )
            conn.commit()

    def create_short_url(self, original_url, short_code):
        expires_at = datetime.utcnow() + timedelta(days=Config.URL_EXPIRE_DAYS)
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                if not original_url or not short_code:
                    raise ValueError("URL and short code cannot be empty")

                cursor.execute(
                    """
                    INSERT INTO urls (original_url, short_code, expires_at)
                    VALUES (?, ?, ?)
                    """,
                    (original_url, short_code, expires_at),
                )
                conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error creating short URL: {e}")
            raise ValueError("URL already exists")
        except sqlite3.Error as e:
            print(f"Error creating short URL: {e}")
            raise

    def get_original_url(self, short_code):
        current_time = datetime.utcnow()
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            if not short_code:
                return None

            cursor.execute(
                """
                SELECT original_url
                FROM urls INDEXED BY idx_short_code
                WHERE short_code = ? AND expires_at > ?
                """,
                (short_code, current_time),
            )
            result = cursor.fetchone()
            return result["original_url"] if result else None

    def get_short_url(self, original_url):
        current_time = datetime.utcnow()
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            if not original_url:
                return None

            cursor.execute(
                """
                SELECT short_code
                FROM urls
                WHERE original_url = ? AND expires_at > ?
                """,
                (original_url, current_time),
            )
            result = cursor.fetchone()
            return result["short_code"] if result else None

    def delete_expired_urls(self):
        current_time = datetime.utcnow()
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                DELETE FROM urls
                WHERE expires_at <= ?
                """,
                (current_time,),
            )
            conn.commit()
