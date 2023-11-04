"""
This is doc
"""
from ..schemas import RefreshTokenSchema
from core.exceptions.token import DecodeTokenException
from core.utils.token_helper import TokenHelper


class JwtService:
    """_summary_
    """
    async def verify_token(self, token: str) -> None:
        """_summary_

        Args:
            token (str): _description_
        """
        TokenHelper.decode(token=token)

    async def create_refresh_token(
        self,
        token: str,
        refresh_token: str,
    ) -> RefreshTokenSchema:
        """_summary_

        Args:
            token (str): _description_
            refresh_token (str): _description_

        Raises:
            DecodeTokenException: _description_

        Returns:
            RefreshTokenSchema: _description_
        """
        token = TokenHelper.decode(token=token)
        refresh_token = TokenHelper.decode(token=refresh_token)
        if refresh_token.get("sub") != "refresh":
            raise DecodeTokenException

        return RefreshTokenSchema(
            token=TokenHelper.encode(payload={"user_id": token.get("user_id")}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )
