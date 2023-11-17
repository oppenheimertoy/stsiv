"""
"""
from pydantic import (
    BaseModel,
    Field,
    constr,
)


class CreateExperimentRequest(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    name: constr(min_length=4, max_length=20)
    description: str = Field(
        str, description="Researching new theory about...")
