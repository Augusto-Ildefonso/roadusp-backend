import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

class Settings:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000").rstrip("/")
    RESET_TOKEN_EXPIRES = int(os.getenv("RESET_TOKEN_EXPIRES", "30"))

settings = Settings()
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)