from django.conf import settings

from api.api_v1.endpoints import posts
from api.main import register_fast_api_application

api_router = register_fast_api_application("/api")

# API endpoints
api_router.include_router(posts.router, prefix="/v1/posts", tags=["posts"])
