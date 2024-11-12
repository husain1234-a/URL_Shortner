import sqlite3
from datetime import datetime, timedelta
from config.settings import Config


class Database:
    def __init__(self):
        self.db_path = Config.DATABASE

    def get_db_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS urls (
                    original_url TEXT PRIMARY KEY,
                    short_code TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL
                )
                """
            )
            conn.commit()

    def create_short_url(self, original_url, short_code):
        expires_at = datetime.now() + timedelta(days=Config.URL_EXPIRE_DAYS)
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
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
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT original_url
                FROM urls
                WHERE short_code = ? AND expires_at > ?
                """,
                (short_code, datetime.now()),
            )
            result = cursor.fetchone()
            return result["original_url"] if result else None

    def get_short_url(self, original_url):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT short_code
                FROM urls
                WHERE original_url = ?
                """,
                (original_url,),
            )
            result = cursor.fetchone()
            return result["short_code"] if result else None
