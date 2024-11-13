import os


class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DATABASE = os.path.join(BASE_DIR, "instance", "url_shortener.db")
    SECRET_KEY = "url-shortener-POC"
    URL_EXPIRE_DAYS = 90
    SHORT_CODE_LENGTH = 8
