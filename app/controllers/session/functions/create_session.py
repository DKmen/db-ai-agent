from uuid import UUID
from sqlmodel import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel

from app.models import Session as UserSession
from app.db import engine
from app.helper import logger

class CreateSessionPayload(BaseModel):
    """
    Payload for creating a new user session.
    Contains the user ID and database connection URL.
    """
    name: str
    user_id: UUID
    db_connection_url: str

def create_session_controller(payload: CreateSessionPayload) -> UUID:
    """
    Controller function to create a new user session in the system.
    Args:
        user_id (UUID): The ID of the user for whom the session is being created.
        db_connection_url (str): The database connection URL for the session.
    Returns:
        UUID: The ID of the created session.
    Raises:
        SQLAlchemyError: If there is an error during the database operation.
        Exception: For any other unexpected errors.
    """
    try:
        logger.info({
            "action": "create_session_controller",
            "payload": payload.dict()
        })
        
        # Create a new session instance
        with Session(engine) as session:
            new_session = UserSession(
                user_id=payload.user_id,
                db_connection_url=payload.db_connection_url,
                name=payload.name
            )
            
            session.add(new_session)
            session.commit()
            session.refresh(new_session)
            
            session.close()
        
        # Log the successful creation of the session
        logger.info({
            "action": "create_session_controller - success",
            "session_id": str(new_session.id),
            "user_id": str(new_session.user_id),
            "db_connection_url": new_session.db_connection_url
        })
        
        # Return the created session ID
        return new_session.id
    
    except SQLAlchemyError as e:
        logger.error({
            "action": "create_session_controller_sqlalchemy_error",
            "user_id": str(payload.user_id),
            "db_connection_url": payload.db_connection_url,
            "error": str(e)
        })
        raise e
    
    except Exception as e:
        logger.error({
            "action": "create_session_controller - error",
            "user_id": str(payload.user_id),
            "db_connection_url": payload.db_connection_url,
            "error": str(e)
        })
        raise e
