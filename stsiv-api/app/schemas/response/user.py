from pydantic import UUID4, BaseModel, Field


class UserResponse(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    id: UUID4 = Field(..., example="a3b8f042-1e16-4f0a-a8f0-421e16df0a2f")
    email: str = Field(..., example="john.doe@example.com")
    username: str = Field(..., example="john.doe")

    class Config:
        from_attributes = True
