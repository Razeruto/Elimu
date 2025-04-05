import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    # Secret Key for JWT Authentication
    SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")

    # OpenAI API Key
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key")

    # MySQL Database Configuration
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "elimu")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "your_mysql_password")
    MYSQL_DB = os.getenv("MYSQL_DB", "elimu_db")

    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/elimu_mongo")

