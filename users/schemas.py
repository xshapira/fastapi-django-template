from django.db import models
from django.forms.models import model_to_dict
from pydantic import BaseModel as _BaseModel
from pydantic import EmailStr, SecretStr, validator

from posts.schemas import BlogPostOutput
from users.models import User


class BaseModel(_BaseModel):
    @classmethod
    def from_orms(cls, instances: list[models.Model]):
        """
        Take a list of Django models and returns a list of Pydantic models.
        This method iterates through the list of instances and calls
        the from_orm method for each instance, converting them to
        related Pydantic models.
        """
        return [cls.from_orm(inst) for inst in instances]


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
