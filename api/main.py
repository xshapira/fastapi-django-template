import functools
from collections.abc import Callable
from typing import Any

from django.conf import settings
from fastapi import APIRouter as FastAPIRouter
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.types import DecoratedCallable
from pydantic import BaseModel

from config.asgi import get_starlette_application


class Error(BaseModel):
    message: str
    type: str


class ErrorResponse(BaseModel):
    detail: list[Error]


def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Format the pydantic ValidationErrors in a more human-readable way.
    """
    errors = {
        "detail": [  # noqa: B035
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
    In your api.py, etc. files, you can do this:

        api_router = register_fast_api_application(settings.API_V1_STR)
        api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
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
        openapi_url="/openapi.json",
        **kwargs,
    )
    application.mount(root_path, fast_api_application)
    return fast_api_application


@functools.cache
class APIRouter(FastAPIRouter):
    def api_route(
        self, path: str, *, include_in_schema: bool = True, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """
        This meant to prevent the 307 Temporary Redirect when there's
        a missing trailing slash. The api_route function is a decorator
        that adds the decorated function to the FastAPI router with
        the given path. If the path ends with a "/", then an additional route
        is added with the trailing slash stripped off.

        We should keep in mind that if we want to use an empty path
        with a router prefix, we need to specify an empty path, not "/":

        router = APIRouter(prefix="/api/v1/posts")

        @router.post("")
        def create_post(post: Post):
        # ...

        :param self: access the class instance
        :param path:str: specify the path to be used for this route
        :param *: pass in any keyword arguments that are not explicitly
        defined by the function
        :param include_in_schema:bool=True: tell fastapi whether or
        not to include the route in the openapi schema
        :param **kwargs:Any: pass any additional keyword arguments to
        the api_route function
        :return: a decorator that adds a path to the api schema
        """
        if path == "/":
            return super().api_route(
                path, include_in_schema=include_in_schema, **kwargs
            )
        path = path.removesuffix("/")
        add_path = super().api_route(
            path, include_in_schema=include_in_schema, **kwargs
        )

        alternate_path = f"{path}/"
        add_alternate_path = super().api_route(
            alternate_path, include_in_schema=False, **kwargs
        )

        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            add_alternate_path(func)
            return add_path(func)

        return decorator
