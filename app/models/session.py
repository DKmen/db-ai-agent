from uuid import UUID
from sqlmodel import Field

from .base import BaseModel

class Session(BaseModel, table=True):
    """
    Session model for tracking user sessions in the application.
    Inherits common fields from BaseModel including id, created_at, updated_at, is_active.
    """
    
    __tablename__ = "sessions"
    
    name: str = Field(
        description="Name of the session",
        max_length=100,
        index=True
    )
    
    # Foreign key to user
    user_id: UUID = Field(
        foreign_key="users.id",
        description="ID of the user who owns this session",
        index=True
    )
    
    # db crediantials
    db_connection_url: str = Field(
        description="Database host for the session",
        max_length=255,
        index=True
    )
