"""
"""
from pydantic import (
    BaseModel,
    Field,
)

from typing import (
    Optional
)


class CreateVersionRequest(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    
    name: Optional[str | None]
    description: str = Field(str, description="In this version we changed...")
