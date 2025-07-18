from uuid import UUID
from sqlmodel import Field
from enum import Enum

from .base import BaseModel

class MessageRole(str, Enum):
    """Enumeration for message role values."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"

class SessionChat(BaseModel, table=True):
    """
    SessionChat model for storing chat conversations within user sessions.
    Tracks individual messages and conversation context.
    """
    
    __tablename__ = "session_chats"
    
    # Foreign keys
    session_id: UUID = Field(
        foreign_key="sessions.id",
        description="ID of the session this chat belongs to",
        index=True
    )
    
    # Message content
    message: str = Field(
        description="The chat message content"
    )
    
    role: MessageRole = Field(
        description="Role of the message sender (user, assistant, system)"
    )
    
    is_final_message: bool = Field(
        default=False,
        description="Indicates if this is the final message in the session chat"
    )
