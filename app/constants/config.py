import os

config = {
    "DB_USER": os.getenv("DB_USER","postgres"),
    "DB_PASSWORD": os.getenv("DB_PASSWORD","password"),
    "DB_HOST": os.getenv("DB_HOST","localhost"),
    "DB_PORT": os.getenv("DB_PORT","5432"),
    "DB_NAME": os.getenv("DB_NAME","anvoon_local"),
    "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY",""),
    "GEMINI_MODEL_ID" : os.getenv("GEMINI_MODEL_ID","gemini-2.0-flash"),
}
