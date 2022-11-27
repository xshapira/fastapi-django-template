from django.conf import settings

from api.main import register_fast_api_application
from posts.routers import router as post_router

api_router = register_fast_api_application(settings.API_V1_STR)

# API endpoints
api_router.include_router(post_router, prefix="/posts", tags=["posts"])
