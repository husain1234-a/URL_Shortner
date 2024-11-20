from locust import HttpUser , TaskSet, task, between
import random
import string
import sqlite3
from datetime import datetime, timedelta
from config.settings import Config

# def random_url():
   
#     # return f"http://www.example.com/{''.join(random.choices(string.ascii_letters + string.digits, k=10))}"
#     return "https://www.geeksforgeeks.org/courses/dsa-to-development-coding-guide?itm_source=geeksforgeeks&itm_medium=main_header&itm_campaign=courses"
class Database:
    def __init__(self):
        self.db_path = Config.DATABASE

    def get_db_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    def random_short_code(self):
     random_number = random.randint(1, 20)
     with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT short_code
                FROM urls
                WHERE rowid = ?
                """,
                (f"{random_number}"),
            )
            result = cursor.fetchone()
            return result["short_code"]
    # return ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    def random_url(self):
        random_number = random.randint(1, 20)
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT original_url
                FROM urls
                WHERE rowid = ?
                """,
                (f"{random_number}"),
            )
            result = cursor.fetchone()
            return result["original_url"]
   
    # return f"http://www.example.com/{''.join(random.choices(string.ascii_letters + string.digits, k=10))}"
    #  return "https://www.geeksforgeeks.org/courses/dsa-to-development-coding-guide?itm_source=geeksforgeeks&itm_medium=main_header&itm_campaign=courses"

class UserBehavior(TaskSet):
     
    db = Database()
    @task(1)
    def shorten_url(self):
        db = Database()
        original_url = db.random_url() 
        response = self.client.post("/", data={"url": original_url})
        print(f"Shortened URL request for {original_url} returned status code {response.status_code}")

    @task(2)
    def access_short_url(self):
        db = Database()
        short_code = db.random_short_code() 
        response = self.client.get(f"/{short_code}")
        print(f"Accessing short URL with code {short_code} returned status code {response.status_code}")

class WebsiteUser (HttpUser ):
    tasks = [UserBehavior]
    wait_time = between(1, 5)