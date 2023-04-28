from typing import Any

from asgiref.sync import sync_to_async
from django.contrib.auth.hashers import make_password
from fastapi import APIRouter, HTTPException

from users.models import User
from users.schemas import UserCreate, UserOutput

router = APIRouter()


@router.get("/", response_model=list[UserOutput])
def get_users() -> list[UserOutput]:
    # We need to convert the queryset of Django models into a list of
    # UserOutput objects. We can achieve this by using the from_orm method
    # we've defined in the UserOutput class.

    user_queryset = User.objects.all()
    return UserOutput.from_orms(user_queryset)


@router.get("/{user_id}", response_model=UserOutput)
def get_user(user_id: int) -> Any:
    return User.objects.get(id=user_id)


@router.post("/", response_model=UserOutput)
async def create_user(user: UserCreate):
    # Check if the email is unique
    email_is_unique = (
        await sync_to_async(User.objects.filter(email=user.email).exists)(),
    )
    if email_is_unique:
        raise HTTPException(status_code=400, detail="Email address already exists")

    # Hash the password
    hashed_password = make_password(user.password.get_secret_value())
    new_user = await sync_to_async(User.objects.create)(
        name=user.name,
        email=user.email,
        password=hashed_password,
    )
    return new_user
