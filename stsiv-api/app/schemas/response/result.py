from pydantic import BaseModel, Field
from typing import Any
from uuid import UUID


class GetResultSchema(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    id: UUID = Field(UUID)
    version_id: UUID = Field(UUID)
    test_id: UUID = Field(UUID)
    name: str = Field(str)

    class Config:
        from_attributes = True
