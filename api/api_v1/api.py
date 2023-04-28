from django.conf import settings

from api.main import register_fast_api_application
from users.router import router as user_router

api_router = register_fast_api_application(settings.API_V1_STR)

# API endpoints
api_router.include_router(user_router, prefix="/users", tags=["users"])
