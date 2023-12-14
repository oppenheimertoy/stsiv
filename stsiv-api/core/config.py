"""
Module contains configuration params
"""
import os
from typing import List, Optional, TypeVar

from functools import lru_cache

from pydantic import field_validator, ValidationInfo
from pydantic.networks import PostgresDsn, MultiHostUrl
from pydantic_settings import BaseSettings
from dotenv import find_dotenv

from .utils.url_builder import URLBuilder


class AppConfig(BaseSettings):
    """
    Application configuration class. It contains the main 
    parameters necessary for connecting to 
    external services. These parameters are retrieved 
    from environment variables.

    Attributes:
        CORS_ORIGINS (str): Allowed origins for Cross-Origin Resource Sharing.
        CORS_ALLOW_METHODS (List[str]): Allowed methods for CORS.
        CORS_ALLOW_HEADERS (List[str]): Allowed headers for CORS.
        CORS_EXPOSE_HEADERS (List[str]): Headers that browsers are 
        allowed to access.
        POSTGRES_SERVER (str): PostgreSQL server address.
        POSTGRES_USER (str): PostgreSQL username.
        POSTGRES_PASSWORD (str): PostgreSQL password.
        POSTGRES_DB (str): PostgreSQL database name.
        SQLALCHEMY_DATABASE_URI (Optional[PostgresDsn]): SQLAlchemy connection 
        string to 
            PostgreSQL database.
        SERVER_HOST (str): The host of the server.
        SERVER_PORT (int): The port of the server.
        MINIO_HOST (Optional[str]): The host of the MinIO server.
        MINIO_PORT (Optional[str]): The port of the MinIO server.
        BUCKET (str): The name of the bucket in the MinIO server.
        SECRET_KEY (str): The secret key for the MinIO server.
        ACCESS_KEY (str): The access key for the MinIO server.
        SSL_CERT_FILE (Optional[str]): The path to the SSL certificate file.
        ENDPOINT_URL (Optional[str]): The endpoint URL for the MinIO server.
        APP_HASH (str): The hash for the Telegram application.
        APP_ID (int): The ID for the Telegram application.
        SESSION_STRING (str): The session string for the Telegram application.

    Methods:
        assemble_db_connection: Assembles the SQLAlchemy 
        connection string from the PostgreSQL parameters.
        assemble_minio_connection: Assembles the endpoint 
        URL from the MinIO parameters.
    """
    ENVIRONMENT: str = "dev"
    # CORS settings
    CORS_ORIGINS: str = "*"
    CORS_ALLOW_METHODS: List[str] = [
        "GET",
        "PUT",
        "PATCH",
        "POST",
        "DELETE",
        "OPTIONS",
        "HEAD",
    ]
    CORS_ALLOW_HEADERS: List[str] = [
        "Content-Type",
        "Authorization",
        "Access-Control-Allow-Origin"
    ]
    CORS_EXPOSE_HEADERS: List[str] = [
        "Cache-Control",
        "Content-Language",
        "Content-Length",
        "Content-Type",
        "Last-Modified",
        "Content-Range",
    ]
    # PostgreSQL connections
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    SQLALCHEMY_ASYNC_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_ASYNC_DATABASE_URI")
    @classmethod
    def assemble_async_db_connection(cls, val: str,
                                     info: ValidationInfo) -> PostgresDsn:
        """
        Assemble async connection string for PostgreSQL database
        Using asyncpg lib

        Args:
            val (str): validating env param
            info (FieldValidationInfo): validation fields from env config

        Returns:
            PostgresDsn: resulting PostgreSQL async connection string
        """
        if val:
            return val
        return PostgresDsn(MultiHostUrl.build(
            scheme="postgresql+asyncpg",  # using format with dialect
            username=URLBuilder.encode_special_characters(
                info.data["POSTGRES_USER"]),
            password=URLBuilder.encode_special_characters(
                info.data["POSTGRES_PASSWORD"]),
            host=info.data["POSTGRES_SERVER"],
            path=f"{info.data['POSTGRES_DB'] or ''}",
            )
        )
    SEED_PATHS: Optional[str] = "core/database/seeds/params.json,core/database/seeds/tests.json"
    # App startup
    SERVER_HOST: str
    SERVER_PORT: int

    class Config:
        """
        Specify config add-ons
        """
        case_sensitive = True
        env_file = find_dotenv(".env")

    LOG_JSON_FORMAT: bool = False
    LOG_LEVEL: str = "INFO"
    DD_TRACE_ENABLED: bool = False


ConfigT = TypeVar("ConfigT", bound=AppConfig)


class DevelopmentJWTConfig(AppConfig):
    """
    Development config for user service
    Added support for jwt tokens

    Args:
        AppConfig (BaseSettings): Base class of application config
    """
    JWT_LIFETIME: int = 7200
    JWT_SECRET_KEY: str = "c65aba774aacb2bcffeb464b14a9401fab0c1d63ef94c5fe663690f45a35fd8e"
    JWT_ALGORITHM: str = "HS256"


class ProductionConfig(AppConfig):
    pass


class TestingConfig(AppConfig):
    pass


@lru_cache()
def get_config() -> ConfigT:
    """
    Returns different config objects depend of env value 

    Returns:
        ConfigT: resulting app configuration
    """
    config_dict = {
        "dev": DevelopmentJWTConfig,
        "prod": ProductionConfig,
        "test": TestingConfig
    }
    # TODO refactor this line
    config_var = os.environ.get("APP_CONF", "dev")
    res_conf = config_dict[config_var]
    return res_conf()


config = get_config()
