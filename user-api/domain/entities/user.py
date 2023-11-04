"""
This module contains User model implementation
"""
from uuid import uuid4, UUID
import bcrypt

from sqlalchemy import String, Boolean
from sqlalchemy import UUID as UUID_SQL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.database import Base as BaseModel
from core.database.mixins import TimestampMixin


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
    middlename: Mapped[String] = mapped_column(String)
    active: Mapped[Boolean] = mapped_column(Boolean, default=True)

    @property
    def password(self):
        """
        Propety for password attribute

        Raises:
            AttributeError: raising attribure error if password is corrupted
        """
        # TODO add custom exception here
        raise AttributeError("Password is not readable.")

    @password.setter
    def password(self, password: str) -> None:
        """
        Password attribute setter

        Args:
            password (str): user password
        """
        self._password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password: str) -> bool:
        """
        Comparing input password with hash in database

        Args:
            password (str): validated password

        Returns:
            _type_: _description_
        """
        return bcrypt.checkpw(password.encode('utf-8'), self._password.encode('utf-8'))

    def __repr__(self):
        return f"<User(user)(user_id={self.id}, username={self.username}, \
            email={self.email}, status={self.active})"
