import asyncio
import concurrent.futures
from typing import Optional

from asgiref.sync import sync_to_async
from dantico import ModelSchema
from pydantic import BaseConfig, BaseModel, validator

from cities.models import City, Programmer

BaseConfig.arbitrary_types_allowed = True


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


class CitySchema(ModelSchema):
    class Config:
        model = City
        include = ["city"]


class ProgrammerSchema(ModelSchema):
    """My model schema"""

    class Config:
        model = Programmer
        include = ["name", "password", "age", "company"]
        # optional = ["company"]
        # 'depth' argument allows us to introspect the Django model
        # into the Related fields(ForeignKey, OneToOne, ManyToMany).
        depth = 0
        title = "Programmer schema"

    @validator("name", check_fields=False, pre=True)
    def validate_name(cls, v):
        """
        Here we are using async method as validator. Because there is
        already an event loop (using FastAPI), we need to start another thread.

        :param cls: Access the class of the object that is being validated
        :param v: Validate the value
        :return: The result of the name_must_be_unique function
        """

        @sync_to_async
        def name_must_be_unique():
            if Programmer.objects.filter(name__icontains=v).exists():
                raise ValueError("name already exists")
            return v

        # A way to run async code in a sync environment.
        pool = concurrent.futures.ThreadPoolExecutor(1)
        result = pool.submit(asyncio.run, name_must_be_unique()).result()

        return result
