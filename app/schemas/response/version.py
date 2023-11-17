from pydantic import BaseModel, Field
from typing import Any
from uuid import UUID

class GetVersionSchema(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    id: UUID =  Field(UUID)
    experiment_id: UUID = Field(UUID)
    name: str = Field(str)
    description: str = Field(str)
    params: Any = Field(..., description="params for certain version")
    
    class Config: 
        from_attributes = True