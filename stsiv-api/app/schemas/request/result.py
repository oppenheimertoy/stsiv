from uuid import UUID
from typing import (
    Optional,
    List,
    Union
)

from pydantic import (
    BaseModel,
    Field,
)


class ListResultsRequest(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    version_id: UUID = Field(UUID)
