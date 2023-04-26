import asyncio
from typing import Optional

from asgiref.asyncio import coroutine
from pydantic import BaseModel, validator
from src.posts.schemas import BlogPostOutput

from users.models import User


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str

    @validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")

        return value

    @validator("email", check_fields=False, pre=True)
    def validate_email(cls, v):
        """
        We use the asyncio.run_coroutine_threadsafe function to run
        the email_must_be_unique function in a separate thread. This
        will prevent the main thread from being blocked.

        Using @coroutine is equivalent to the code that uses the
        @sync_to_async decorator. But, using @coroutine decorator
        is more efficient, because it does not need to start
        a separate thread to execute the function.

        :param cls: Access the class of the object that is being validated
        :param v: Validate the value
        :return: The result of the email_must_be_unique function
        """

        @coroutine
        def email_must_be_unique():
            if User.objects.filter(email=v).exists():
                raise ValueError("email address already exists")
            return v

        result = asyncio.run_coroutine_threadsafe(
            email_must_be_unique(),
            loop=asyncio.get_event_loop(),
        )

        return result


class UserOutput(UserBase):
    id: int
    posts: list["BlogPostOutput"] | None

    class Config:
        model = User


class UserUpdate(UserBase):
    password: str
