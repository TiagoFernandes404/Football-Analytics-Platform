from dotenv import load_dotenv
import os

load_dotenv()
#we go and get our secret information from the .env
API_KEY = os.getenv("API_KEY")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
# the free plan of the api allows 10 request per minute so we put a delay of 
# 7 sec to ensure we are safe and not hitting that timer 
# max_retries is 3 because if it fails 3 times is prob not working soooo ahha 
RATE_LIMIT_DELAY = 7
MAX_RETRIES = 3