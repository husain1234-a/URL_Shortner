import string
import random
from config.settings import Config
from database.db import Database


def generate_short_code(length=None):
    if length is None:
        length = Config.SHORT_CODE_LENGTH

    characters = string.ascii_letters + string.digits
    url_model = Database()

    while True:
        short_code = "".join(random.choices(characters, k=length))
        conn = url_model.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM urls WHERE short_code = ?", (short_code,))
        exists = cursor.fetchone() is not None
        conn.close()

        if not exists:
            return short_code

