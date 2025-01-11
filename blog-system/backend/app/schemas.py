from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BlogPostBase(BaseModel):
    title: str = Field(..., max_length=200)
    content: str
    meta_description: Optional[str] = Field(None, max_length=160)
    keywords: Optional[str] = Field(None, max_length=200)
    is_published: bool = True

class BlogPostCreate(BlogPostBase):
    pass

class BlogPost(BlogPostBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
