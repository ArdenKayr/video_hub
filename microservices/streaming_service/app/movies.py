    from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/", response_model=List[schemas.MovieResponse])
async def get_movies(
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Получить список фильмов"""
    query = db.query(models.Movie)
    
    if category:
        query = query.join(models.Category).filter(
            models.Category.slug == category
        )
    
    movies = query.offset(skip).limit(limit).all()
    return movies

@router.get("/{slug}", response_model=schemas.MovieResponse)
async def get_movie(slug: str, db: Session = Depends(get_db)):
    """Получить фильм по slug"""
    movie = db.query(models.Movie).filter(
        models.Movie.slug == slug
    ).first()
    
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return movie

@router.get("/{slug}/stream-info", response_model=schemas.MovieStreamInfo)
async def get_stream_info(slug: str, db: Session = Depends(get_db)):
    """Получить информацию о стриме"""
    movie = db.query(models.Movie).filter(
        models.Movie.slug == slug
    ).first()
    
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    stream_url = None
    if movie.video_file:
        stream_url = f"/api/v1/stream/{slug}"
    elif movie.video_url:
        stream_url = movie.video_url
    
    return schemas.MovieStreamInfo(
        movie_id=movie.id,
        title=movie.title,
        has_video_file=bool(movie.video_file),
        has_video_url=bool(movie.video_url),
        stream_url=stream_url
    )