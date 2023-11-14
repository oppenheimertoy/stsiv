"""
This module initializes the application using factory app method
"""
import time
from fastapi import FastAPI, Request, Response
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from fastapi.responses import JSONResponse

from typing import List

from starlette.middleware.authentication import (
    AuthenticationMiddleware
)

from core.config import config
from core.containers.base_container import BaseContainer
from core.exceptions.base import CustomException
from core.logging.logging_pretty import setup_logging
from core.middleware.auth_middleware import (
    AuthBackend
)

from core.middleware.logging_middleware import logging_middleware

from api import router

import structlog
from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.context import correlation_id

from ddtrace.contrib.asgi.middleware import TraceMiddleware
from uvicorn.protocols.utils import get_path_with_query_string


def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_headers=config.CORS_ALLOW_HEADERS,
            allow_methods=config.CORS_ALLOW_METHODS,
            allow_origins=config.CORS_ORIGINS,
            expose_headers=config.CORS_EXPOSE_HEADERS
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
        Middleware(CorrelationIdMiddleware)
    ]
    return middleware


def create_app() -> FastAPI:
    """
    Creates and configures the FastAPI application.

    Returns:
        FastAPI: The created FastAPI application.
    """
    # initialsing base container for dependencies injections
    container = BaseContainer()

    db_inst = container.async_db
    
    seeder = BaseContainer.seeder

    setup_logging(json_logs=config.LOG_JSON_FORMAT, log_level=config.LOG_LEVEL)


    factory_app = FastAPI(openapi_url="/api/v1/openapi.json",
                          title="media_ml",
                          swagger_ui_oauth2_redirect_url="/api/v1/docs/oauth2-redirect",
                          debug=True,
                          middleware=make_middleware())

    factory_app.middleware("http")(logging_middleware)
    tracing_middleware = next(
        (m for m in factory_app.user_middleware if m.cls == TraceMiddleware), None
    )
    if tracing_middleware is not None:
        factory_app.user_middleware = [
            m for m in factory_app.user_middleware if m.cls != TraceMiddleware]
        structlog.stdlib.get_logger("api.datadog_patch").info(
            "Patching Datadog tracing middleware to be the outermost middleware..."
        )
        factory_app.user_middleware.insert(0, tracing_middleware)
        factory_app.middleware_stack = factory_app.build_middleware_stack()

    factory_app.include_router(router)

    @factory_app.get("/api/v1/docs", include_in_schema=False)
    async def get_documentation():
        return get_swagger_ui_html(openapi_url="openapi.json", title="Swagger")

    @factory_app.on_event("startup")
    async def startup_event():
        await db_inst.create_database()
        await seeder.create_seeds()

    @factory_app.on_event("shutdown")
    async def shutdown_db_connection():
        await db_inst.close_database_connection()

    return factory_app


app = create_app()
