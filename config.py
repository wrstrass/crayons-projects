import os
from dotenv import load_dotenv

load_dotenv()


PREFIX = "/api/v1"

AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
JWT_ACCESS_EXPIRE_TIME = int(os.getenv("JWT_ACCESS_EXPIRE_TIME"))

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
