import asyncio

from asgiref.sync import sync_to_async
from pydantic import BaseModel, validator

from posts.schemas import BlogPostOutput
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
        Using @sync_to_async decorator helps us to convert synchronous code
        into asynchronous code. @sync_to_async decorator works by wrapping
        the synchronous code in a coroutine. The coroutine will then be run
        in an asynchronous environment. This will allow the synchronous code
        to run concurrently with other tasks.

        We also use the asyncio.run_coroutine_threadsafe function to run
        the email_must_be_unique function in a separate thread. This
        will prevent the main thread from being blocked.

        :param cls: Access the class of the object that is being validated
        :param v: Validate the value
        :return: The result of the email_must_be_unique function
        """

        @sync_to_async
        async def email_must_be_unique():
            if await User.objects.filter(email=v).exists():
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
