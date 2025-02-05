import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000/api")
    # Add other configuration variables here

settings = Settings()