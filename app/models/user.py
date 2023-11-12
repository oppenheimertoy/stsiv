"""
This module contains User model implementation
"""
from uuid import uuid4, UUID
import bcrypt

from sqlalchemy import String, Boolean
from sqlalchemy import UUID as UUID_SQL
from sqlalchemy.orm import Mapped, mapped_column

from core.database.database import Base as BaseModel
from core.database.mixins.timestamps import TimestampMixin


class User(BaseModel, TimestampMixin):
    """
    This class is implementation of User model
    Args:
        BaseModel (metaclass): declarative base
    """
    __tablename__ = 'users'
    id: Mapped[UUID] = mapped_column(
        UUID_SQL, primary_key=True, default=uuid4())
    username: Mapped[String] = mapped_column(String, unique=True)
    email: Mapped[String] = mapped_column(String, unique=True)
    _password: Mapped[String] = mapped_column("password", String)
    name: Mapped[String] = mapped_column(String)
    surname: Mapped[String] = mapped_column(String)
    active: Mapped[Boolean] = mapped_column(Boolean, default=True)

    @property
    def password(self) -> str:
        """
        Propety for password attribute

        Raises:
            AttributeError: raising attribure error if password is corrupted
        """
        return self._password
        
    def __repr__(self):
        return f"<User(user)(user_id={self.id}, username={self.username}, \
            email={self.email}, status={self.active})"
