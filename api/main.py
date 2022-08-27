import functools
from typing import List

from django.conf import settings
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from config.asgi import get_starlette_application


class Error(BaseModel):
    # loc: Optional[List[str]] = None
    message: str
    type: str


class ErrorResponse(BaseModel):
    detail: List[Error]


def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Format the pydantic ValidationErrors in a more human-readable way.
    """
    errors = {
        "detail": [
            {
                "message": err["msg"],
                "type": err["type"],
            }
        ]
        for err in exc.errors()
    }
    error_res = ErrorResponse(**errors)
    return JSONResponse(
        content=jsonable_encoder(error_res.detail[0]),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@functools.cache
def register_fast_api_application(root_path: str, **kwargs) -> FastAPI:
    """
    In your views.py, etc. files, you can do this:
        app = register_fast_api_application("/api/v1/")
        @app.get("/hello")
        def hello():
            return {"hello": "world"}
    """
    application = get_starlette_application()
    fast_api_application = FastAPI(
        root_path=root_path,
        debug=settings.DEBUG,
        exception_handlers={RequestValidationError: validation_exception_handler},
        responses={
            422: {
                "description": "Validation Error",
                "model": ErrorResponse,
            },
        },
        title="My API",
        description="Some description here",
        **kwargs,
    )
    application.mount(root_path, fast_api_application)
    return fast_api_application
