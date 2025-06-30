from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.controllers.chat import router as chat_router
from app.controllers.session import router as session_router
from app.controllers.user import router as user_router

load_dotenv()

app = FastAPI(title="DB Retrieval", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api/v1", tags=["Chat"])
app.include_router(session_router, prefix="/api/v1", tags=["Session"])
app.include_router(user_router, prefix="/api/v1", tags=["User"])
