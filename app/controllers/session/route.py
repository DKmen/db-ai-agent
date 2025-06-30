from fastapi import APIRouter
from .functions import create_session_controller, CreateSessionPayload, get_user_session_controller

router = APIRouter(prefix="/session", tags=["Session"])

@router.post("/create")
def create_session_route(session_data: CreateSessionPayload):
    """Route to create a new session.
    Args:
        session_data (CreateSessionPayload): The data of the session to create.
    Returns:
        The response from the session creation controller.
    """

    return create_session_controller(session_data)

@router.get("/{user_id}")
def get_user_session_route(user_id: str):
    """Route to get all sessions for a user.
    Args:
        user_id (str): The ID of the user whose sessions are to be retrieved.
    Returns:
        The response from the session retrieval controller.
    """
    
    return get_user_session_controller(user_id)
