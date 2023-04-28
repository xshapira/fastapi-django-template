from typing import Any

from asgiref.sync import sync_to_async
from django.contrib.auth.hashers import make_password
from fastapi import APIRouter, HTTPException

from users.models import User
from users.schemas import UserCreate, UserOutput

router = APIRouter()


@router.get("/", response_model=list[UserOutput])
def get_users() -> list[UserOutput]:
    return User.objects.all()


@router.get("/{user_id}", response_model=UserOutput)
def get_user(user_id: int) -> Any:
    return User.objects.get(id=user_id)


# @router.post("/", response_model=UserOutput)
# def create_user(user: UserCreate):
#     # Hash the password
#     hashed_password = make_password(user.password.get_secret_value())
#     new_user = User.objects.create(
#         name=user.name,
#         email=user.email,
#         password=hashed_password,
#     )
#     print("New user created:", new_user)
#     return new_user


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


# @router.put("/{user_id}", response_model=UserOutput)
# def update_user(user_id: int, input: UserUpdate, user: User) -> Any:
#     user = user.objects.get(id=user_id)

#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found.")

#     try:
#         for key, value in input.dict(exclude_unset=True).items():
#             setattr(user, key, value)
#         db.commit()
#     except IntegrityError as e:
#         raise HTTPException(status_code=409, detail="Email already exists.") from e
#     return user


# @router.delete("/{user_id}", response_model=UserOutput)
# def delete_user(user_id: int, db: Annotated[QuerySet[User], Depends(get_db)]) -> Any:
#     user = db.get(id=user_id)

#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found.")

#     db.delete(user)
#     db.commit()

#     return JSONResponse(
#         content={"message": "User deleted successfully"}, status_code=200
#     )


# # This is a new endpoint that was added to the API.
# @router.get("/users/{user_id}/posts", response_model=list[BlogPostOutput])
# def get_user_posts(user_id: int, db: Annotated[QuerySet[User], Depends(get_db)]) -> Any:  # noqa: E501
#     posts = db.filter(User.id == user_id).values("posts__title").distinct()
#     return posts
