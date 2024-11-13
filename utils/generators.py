import time
import string
import hashlib
from database.db import Database
from config.settings import Config


def generate_short_code(length=None):
    if length is None:
        length = Config.SHORT_CODE_LENGTH

    def base62_encode(num):
        chars = string.digits + string.ascii_uppercase + string.ascii_lowercase
        base = len(chars)
        result = ""
        while num:
            num, rem = divmod(num, base)
            result = chars[rem] + result
        return result or "0"

    url_model = Database()

    while True:
        timestamp = str(time.time()).encode("utf-8")
        hash_object = hashlib.sha256(timestamp)
        hash_hex = hash_object.hexdigest()
        hash_int = int(hash_hex[:16], 16)
        short_code = base62_encode(hash_int)[:length]
        conn = url_model.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM urls WHERE short_code = ?", (short_code,))
        exists = cursor.fetchone() is not None
        conn.close()

        if not exists:
            return short_code
