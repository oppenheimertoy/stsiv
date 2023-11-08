from datetime import datetime, timedelta

import jwt

from core.config import config
from core.exceptions import DecodeTokenException, ExpiredTokenException


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
    def encode(payload: dict, expire_period: int = config.JWT_CONFIG) -> str:
        """
        Encoding 

        Args:
            payload (dict): payload of certain jwt
            expire_period (int, optional): Time of life for token. Defaults to 3600.

        Returns:
            str: encoded token
        """
        token = jwt.encode(
            payload={
                **payload,
                "exp": datetime.utcnow() + timedelta(seconds=expire_period),
            },
            key=config.JWT_SECRET_KEY,
            algorithm=config.JWT_ALGORITHM,
        ).decode("utf8")

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
