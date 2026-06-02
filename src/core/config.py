import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

class Settings:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = os.getenv("SMTP_PORT", "587")
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASS = os.getenv("SMTP_PASS")
    EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    RESET_TOKEN_EXPIRES = int(os.getenv("RESET_TOKEN_EXPIRES", "30"))

settings = Settings()
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)