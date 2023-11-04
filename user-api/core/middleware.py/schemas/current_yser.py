"""
"""
from pydantic import BaseModel, Field
from uuid import UUID


class CurrentUser(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    id: UUID = Field(None, description="ID")

    class Config:
        validate_assignment = True
