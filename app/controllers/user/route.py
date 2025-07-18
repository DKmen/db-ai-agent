from fastapi import APIRouter
from .functions import create_user_controller, CreateUserControllerPayload

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/create")
def create_user_route(user_data: CreateUserControllerPayload):
    """Route to create a new user.
    Args:
        user_data (CreateUserControllerPayload): The data of the user to create.
    Returns:
        The response from the user creation controller.
    """

    return create_user_controller(user_data)
