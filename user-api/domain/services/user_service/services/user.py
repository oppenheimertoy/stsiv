from typing import Optional, List

from sqlalchemy import or_, select, and_

from app.user.schemas.user import LoginResponseSchema
from domain.entities.user import User
from infrastructure.repositories.user_repo import UserRepository
from core.db import Transactional, session
from core.exceptions import (
    PasswordDoesNotMatchException,
    DuplicateEmailOrNicknameException,
    UserNotFoundException,
)
from core.utils.token_helper import TokenHelper


class UserService:
    def __init__(self):
        user_repo: UserRepository = UserRepository()

    async def login(self, token: str, password: str) -> LoginResponseSchema:
        result = await session.execute(
            select(User).where(and_(User.email == email, password == password))
        )
        user = result.scalars().first()
        if not user:
            raise UserNotFoundException

        response = LoginResponseSchema(
            token=TokenHelper.encode(payload={"user_id": user.id}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )
        return response

    async def create_user(
        self, email: str, password1: str, password2: str, nickname: str
    ) -> None:
        if password1 != password2:
            raise PasswordDoesNotMatchException

        query = select(User).where(
            or_(User.email == email, User.nickname == nickname))
        result = await session.execute(query)
        is_exist = result.scalars().first()
        if is_exist:
            raise DuplicateEmailOrNicknameException

        user = User(email=email, password=password1, nickname=nickname)
        session.add(user)
