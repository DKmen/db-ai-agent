from pydantic import BaseModel
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models import User
from app.db import engine
from app.helper import logger


class CreateUserControllerPayload(BaseModel):
    email: str
    name: str


class CreateUserError(Exception):
    """Custom exception for user creation errors."""
    def __init__(self, message: str, error_code: str = "USER_CREATION_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


def create_user_controller(user_data: CreateUserControllerPayload):
    """
    Controller function to create a new user in the system.
    
    Args:
        user_data (CreateUserControllerPayload): Data for creating a new user.
        
    Returns:
        User: The created user object.
        
    Raises:
        CreateUserError: When user creation fails with specific error details.
    """
    
    try:
        logger.info({
            "action": "create_user_controller",
            "email": user_data.email,
            "name": user_data.name
        })
        
        # Create a new user instance
        with Session(engine) as session:
            # Check if user with email already exists
            existing_user = session.exec(
                select(User).where(User.email == user_data.email)
            ).first()
            
            if existing_user:
                logger.warning({
                    "action": "create_user_controller_email_exists",
                    "email": user_data.email
                })
                raise CreateUserError(
                    f"A user with email '{user_data.email}' already exists",
                    "EMAIL_ALREADY_EXISTS"
                )
            
            new_user = User(
                email=user_data.email,
                name=user_data.name
            )
            
            # Add the new user to the session
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
        
        # Log the successful creation of the user
        logger.info({
            "action": "create_user_controller - success",
            "user_id": str(new_user.id),
            "email": new_user.email,
            "name": new_user.name
        })
            
        # Return the created user
        return new_user
        
    except IntegrityError as e:
        logger.error({
            "action": "create_user_controller_integrity_error",
            "error": str(e),
            "email": user_data.email,
            "name": user_data.name
        })
        
        # Handle database constraint violations
        if "email" in str(e).lower():
            raise CreateUserError(
                f"Email '{user_data.email}' is already registered",
                "EMAIL_CONSTRAINT_VIOLATION"
            )
        else:
            raise CreateUserError(
                "A database constraint was violated. Please check your input data.",
                "DATABASE_CONSTRAINT_ERROR"
            )
    
    except SQLAlchemyError as e:
        logger.error({
            "action": "create_user_controller_db_error",
            "error": str(e),
            "email": user_data.email,
            "name": user_data.name
        })
        
        raise CreateUserError(
            "Database error occurred while creating user. Please try again.",
            "DATABASE_ERROR"
        )
    
    except Exception as e:
        logger.error({
            "action": "create_user_controller_unexpected_error",
            "error": str(e),
            "error_type": type(e).__name__,
            "email": user_data.email,
            "name": user_data.name
        })
        
        raise CreateUserError(
            f"Unexpected error creating user: {str(e)}",
            "UNEXPECTED_ERROR"
        )
