from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    slug: str

class CategoryResponse(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True

class MovieBase(BaseModel):
    title: str
    slug: str
    description: str
    year: int
    duration: int

class MovieResponse(MovieBase):
    id: int
    poster: Optional[str] = None
    video_url: Optional[str] = None
    video_file: Optional[str] = None
    director: Optional[str] = None
    actors: Optional[str] = None
    views_count: int
    category: Optional[CategoryResponse] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class MovieStreamInfo(BaseModel):
    movie_id: int
    title: str
    has_video_file: bool
    has_video_url: bool
    stream_url: Optional[str] = None