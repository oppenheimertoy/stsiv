from pydantic import BaseModel, Field


class RefreshTokenSchema(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")
