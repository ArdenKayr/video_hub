from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class Movie(Base):
    __tablename__ = "movies_movie"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    slug = Column(String(255), unique=True, index=True)
    description = Column(Text)
    year = Column(Integer)
    duration = Column(Integer)
    poster = Column(String(100))
    video_url = Column(String(200))
    video_file = Column(String(100))
    director = Column(String(255))
    actors = Column(Text)
    category_id = Column(Integer, ForeignKey("movies_category.id"))
    views_count = Column(Integer, default=0)
    created_at = Column(DateTime)
    
    category = relationship("Category")

class Category(Base):
    __tablename__ = "movies_category"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    slug = Column(String(100), unique=True, index=True)