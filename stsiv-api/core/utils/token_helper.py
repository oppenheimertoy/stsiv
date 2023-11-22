from datetime import datetime, timedelta
from uuid import UUID

import jwt

from core.exceptions.jwt import DecodeTokenException, ExpiredTokenException
from ..config import config


class TokenHelper:
    """
    Token Helper implement some functionality for
    jwt tokens

    Raises:
        DecodeTokenException: 
        ExpiredTokenException:
        DecodeTokenException:
    """
    @staticmethod
    def encode(payload: dict, expire_period: int = config.JWT_LIFETIME) -> str:
        """
        Encoding 

        Args:
            payload (dict): payload of certain jwt
            expire_period (int, optional): Time of life for token. Defaults to 3600.

        Returns:
            str: encoded token
        """
        # Convert UUIDs to strings
        payload = {k: str(v) if isinstance(v, UUID)
                   else v for k, v in payload.items()}

        # Add expiration to payload
        payload["exp"] = datetime.utcnow() + timedelta(seconds=expire_period)
        token = jwt.encode(
            payload=payload,
            key=config.JWT_SECRET_KEY,
            algorithm=config.JWT_ALGORITHM
        )

        # Decode token if it's in bytes
        if isinstance(token, bytes):
            token = token.decode("utf-8")

        return token

    @staticmethod
    def decode(token: str) -> dict:
        """_summary_

        Args:
            token (str): _description_

        Raises:
            DecodeTokenException: _description_
            ExpiredTokenException: _description_

        Returns:
            dict: _description_
        """
        try:
            return jwt.decode(
                token,
                config.JWT_SECRET_KEY,
                config.JWT_ALGORITHM,
            )
        except jwt.exceptions.DecodeError:
            raise DecodeTokenException
        except jwt.exceptions.ExpiredSignatureError:
            raise ExpiredTokenException

    @staticmethod
    def decode_expired_token(token: str) -> dict:
        """_summary_

        Args:
            token (str): _description_

        Raises:
            DecodeTokenException: _description_

        Returns:
            dict: _description_
        """
        try:
            return jwt.decode(
                token,
                config.JWT_SECRET_KEY,
                config.JWT_ALGORITHM,
                options={"verify_exp": False},
            )
        except jwt.exceptions.DecodeError:
            raise DecodeTokenException
