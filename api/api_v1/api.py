from django.conf import settings

from api.api_v1.endpoints import cities
from api.main import register_fast_api_application

api_router = register_fast_api_application(settings.API_V1_STR)


# API endpoints
api_router.include_router(
    cities.router, prefix=f"{settings.API_V1_STR}/posts", tags=["posts"]
)
