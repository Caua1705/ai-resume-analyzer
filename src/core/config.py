import os
from dotenv import load_dotenv

load_dotenv()

URL_SUPABASE = os.getenv("DATABASE_URL")