from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict

class BaseModel(SQLModel):
    """
    Base model class that provides common fields and functionality
    for all database models in the application.
    """
    
    model_config = ConfigDict(
        # Allow validation of assignment to attributes
        validate_assignment=True,
        # Use enum values instead of enum names in JSON
        use_enum_values=True,
        # Populate models by name (field name) rather than alias
        populate_by_name=True,
    )
    
    id: Optional[UUID] = Field(
        default_factory=uuid4,
        primary_key=True,
        description="Unique identifier for the record"
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the record was created",
        index=True
    )
    
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the record was last updated",
        index=True
    )
