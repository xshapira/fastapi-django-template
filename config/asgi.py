import functools
import importlib
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # noqa


import anyio
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.db import (
    InterfaceError,
    OperationalError,
    close_old_connections,
    connections,
)
from starlette import status
from starlette.applications import Starlette
from starlette.concurrency import run_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.wsgi import WSGIMiddleware
from starlette.responses import Response

FILES_TO_IMPORT = {
    "api.py",
    "routes.py",
    "views.py",
    "urls.py",
}


def run_once(func):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return func(*args, **kwargs)

    wrapper.has_run = False
    return wrapper


@run_once
def find_and_load_select_modules():
    """
    Use os.walk and importlib.import_module to find all endpoints files
    in settings.BASE_DIR and "import" them such that any @router.get()
    decorators are found and executed properly, before any traffic is
    served.
    """
    for root, dirs, files in os.walk(settings.BASE_DIR):
        files = [f for f in files if f[0] != "."]
        dirs[:] = [d for d in dirs if d[0] != "."]
        for file in files:
            if any(file.endswith(file_to_import) for file_to_import in FILES_TO_IMPORT):
                module_path = os.path.join(root, file)
                module_dir = os.path.dirname(module_path)
                module_rel_path = os.path.relpath(module_dir, settings.BASE_DIR)
                module_rel_path = module_rel_path.replace(os.sep, ".")
                module_name = f"{module_rel_path}." + file.replace(".py", "")
                importlib.import_module(module_name)


def close_connections_for_func(func):
    """
    A decorator that will close all connections after calling the function,
    if it throws an appropriate error.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (OperationalError, InterfaceError):
            close_old_connections()
            raise

    return wrapper


async def smart_sync_to_async(func, *args, **kwargs):
    """
    A Starlette/FastAPI compatible replacement for Django's, with slightly
    different __call__ semantics (drop currying pattern for immediate invoke).
    """
    wrapped_func = close_connections_for_func(func)
    is_starlette = anyio.get_current_task().name.startswith("starlette.")
    if is_starlette:
        return await run_in_threadpool(wrapped_func, *args, **kwargs)
    else:
        return await sync_to_async(wrapped_func)(*args, **kwargs)


class SuppressNoResponseReturnedMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        """
        We are using this middleware to avoid RuntimeError:
        No response returned in FastAPI when refresh request.
        https://github.com/encode/starlette/discussions/1527

        The middleware is just a quick fix (it has to be the last
        middleware that was registered by the call add_middleware)
        to catch the RuntimeError and check that the client is disconnected.
        And then return a dummy response (which the client doesn't read anyway).
        """
        try:
            return await call_next(request)
        except RuntimeError as exc:
            if str(exc) == "No response returned." and await request.is_disconnected():
                return Response(status_code=status.HTTP_204_NO_CONTENT)
            raise


class AsyncCloseConnectionsMiddleware(BaseHTTPMiddleware):
    """
    Using this middleware to call close_old_connections() twice is
    a pretty dirty hack, as it appears that
    run_in_threadpool (used by Starlette/FastAPI) and sync_to_async
    (used by Django) have divergent behavior, ultimately acquiring
    the incorrect thread in mixed sync/async which has the effect
    of duplicating connections.

    We could fix the duplicate connections too if we normalized
    the thread behavior, but at minimum we need to clean up
    connections in each case to prevent persistent
    "InterfaceError: connection already closed" errors when
    the database connection is reset via a database restart
    or something -- so here we are!

    If we always use smart_sync_to_async(), this double calling
    isn't necessary, but depending on what levels of abstraction
    we introduce, we might silently break the assumptions.
    Better to be safe than sorry!
    """

    async def dispatch(self, request, call_next):
        await run_in_threadpool(close_old_connections)
        await sync_to_async(close_old_connections)()
        try:
            response = await call_next(request)
        finally:
            # in tests, use @override_settings(CLOSE_CONNECTIONS_AFTER_REQUEST=True)
            if getattr(settings, "CLOSE_CONNECTIONS_AFTER_REQUEST", False):
                await run_in_threadpool(connections.close_all)
                await sync_to_async(connections.close_all)()
        return response


@functools.cache
def get_starlette_application() -> Starlette:
    return Starlette(debug=settings.DEBUG)


@functools.cache
def get_application() -> Starlette:
    django_application = get_wsgi_application()
    application = get_starlette_application()
    application.add_middleware(AsyncCloseConnectionsMiddleware)
    application.add_middleware(SuppressNoResponseReturnedMiddleware)
    find_and_load_select_modules()  # this must happen before the django mount
    application.mount("/", WSGIMiddleware(django_application))
    return application


# run with `uvicorn config.asgi:application`
application = get_application()
