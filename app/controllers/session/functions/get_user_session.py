from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

from app.models import Session as UserSession
from app.db import engine
from app.helper import logger

def get_user_session_controller(user_id:UUID):
    """
    Controller function to retrieve user sessions from the database.
    Args:
        user_id (UUID): The ID of the user whose sessions are to be retrieved.
    Returns:
        List[UserSession]: A list of user sessions associated with the given user ID.
    Raises:
        SQLAlchemyError: If there is an error during the database operation.
        Exception: For any other unexpected errors.
    """
    try:
        logger.info({
            "action": "get_user_session_controller",
            "user_id": str(user_id)
        })
        
        with Session(engine) as session:
            user_session = session.exec(
                select(UserSession).where(UserSession.user_id == user_id)
            ).all()
            
            if not user_session:
                logger.warning({
                    "action": "get_user_session_controller_no_session",
                    "user_id": str(user_id)
                })
                return None
            
            session.close()
        
        logger.info({
            "action": "get_user_session_controller - success",
            "user_id": str(user_id),
            "session_count": len(user_session)
        })
        
        return user_session
    
    except SQLAlchemyError as e:
        logger.error({
            "action": "get_user_session_controller - error",
            "user_id": str(user_id),
            "error": str(e)
        })
        raise e
    
    except Exception as e:
        logger.error({
            "action": "get_user_session_controller - unexpected error",
            "user_id": str(user_id),
            "error": str(e)
        })
        raise e
