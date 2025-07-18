import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

config = {
    "DB_USER": os.getenv("DB_USER","postgres"),
    "DB_PASSWORD": os.getenv("DB_PASSWORD","postgres"),
    "DB_HOST": os.getenv("DB_HOST","localhost"),
    "DB_PORT": os.getenv("DB_PORT","5433"),
    "DB_NAME": os.getenv("DB_NAME","db_agent"),
    "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY",""),
    "GEMINI_MODEL_ID" : os.getenv("GEMINI_MODEL_ID","gemini-2.0-flash"),
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY",""),
    "OPENAI_MODEL_ID": os.getenv("OPENAI_MODEL_ID","gpt-4o-mini"),
}
