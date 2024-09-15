import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
TOKEN_SECRET = os.getenv("TOKEN_SECRET")
TOKEN_EXPIRATION = int(os.getenv("TOKEN_EXPIRATION"))
TOKEN_ALGORITHM = os.getenv("TOKEN_ALGORITHM")
REDIS_URL = os.getenv("REDIS_URL")