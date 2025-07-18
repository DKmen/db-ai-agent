from fastapi import APIRouter
from uuid import UUID

from .functions import user_chat_controller

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.get("")
def chat_route(session_id: UUID, query: str):
    """Route to handle chat queries.
    Args:
        session_id (UUID): The ID of the session.
        query (str): The chat query to process.
    Returns:
        The response from the chat controller.
    """
    return user_chat_controller(session_id, query)
