from datetime import datetime

from pydantic import BaseModel

from posts.models import BlogPost


class BlogPostBase(BaseModel):
    title: str
    slug: str
    authors: list[str]
    content: str


class BlogPostOutput(BlogPostBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, blog: BlogPost):
        return cls(**blog.dict())


class BlogPostUpdate(BlogPostBase):
    pass
