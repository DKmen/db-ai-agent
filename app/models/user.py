from typing import Optional
from sqlmodel import Field, Relationship
from .base import BaseModel

class User(BaseModel, table=True):
    """
    User model for managing user accounts in the application.
    Inherits common fields from BaseModel including id, created_at, updated_at, is_active.
    """
    
    __tablename__ = "users"
    
    email: str = Field(
        unique=True,
        description="User's email address",
        index=True
    )
    
    name: Optional[str] = Field(
        default=None,
        description="Full name of the user",
        max_length=100
    )
