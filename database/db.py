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
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS urls (
                original_url TEXT PRIMARY KEY,
                short_code TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                visits INTEGER DEFAULT 0
            )
        """
        )
        conn.commit()
        conn.close()

    def create_short_url(self, original_url, short_code):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        expires_at = datetime.now() + timedelta(days=Config.URL_EXPIRE_DAYS)
        # if original_url.exists():
        #     raise ValueError("URL already exists")
        # else:
        #     cursor.execute(
        #         """
        #         INSERT INTO urls (original_url, short_code, expires_at)
        #         VALUES (?, ?, ?)
        #     """,
        #         (original_url, short_code, expires_at),
        #     )
        cursor.execute(
            """
                INSERT INTO urls (original_url, short_code, expires_at)
                VALUES (?, ?, ?)
            """,
            (original_url, short_code, expires_at),
        )

        conn.commit()
        conn.close()

    def get_original_url(self, short_code):
        conn = self.get_db_connection()
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

        conn.close()
        return result["original_url"] if result else None
