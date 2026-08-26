import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://notes_user:notes_pass@localhost:5432/notes_db",
)
API_KEY = os.getenv("API_KEY", "dev-secret-key")