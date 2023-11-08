"""
"""
from pydantic import BaseModel, Field
from uuid import UUID


class CurrentUser(BaseModel):
    """
    Schema for current user used by middleware

    Args:
        BaseModel (_type_): _description_
    """
    id: UUID = Field(None, description="ID")

    class Config:
        validate_assignment = True
