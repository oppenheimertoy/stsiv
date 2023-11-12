from uuid import UUID
from pydantic import BaseModel, Field


class GetUserListResponseSchema(BaseModel):
    id: UUID = Field(..., description="ID")
    email: str = Field(..., description="Email")
    nickname: str = Field(..., description="Nickname")

    class Config:
        orm_mode = True


class LoginResponseSchema(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")


class CurrentUser(BaseModel):
    id: UUID = Field(None, description="User ID")

    class Config:
        validate_assignment = True
