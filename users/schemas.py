from django.forms.models import model_to_dict
from pydantic import BaseModel, EmailStr, SecretStr, validator

from posts.schemas import BlogPostOutput
from users.models import User


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: SecretStr

    @validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")

        return value


class UserOutput(UserBase):
    id: int
    posts: list["BlogPostOutput"] | None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, user: User):
        user_data = model_to_dict(user)
        user_data["posts"] = []
        return cls(**user_data)


class UserUpdate(UserBase):
    password: SecretStr
