from fastapi import APIRouter, HTTPException
import requests
from .. import schemas
from ..config import settings

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/{slug}/stream-info", response_model=schemas.MovieStreamInfo)
async def get_stream_info(slug: str):
    """Получить информацию о стриме из Django API"""
    
    try:
        # Запрашиваем информацию у Django
        response = requests.get(
            f'{settings.DJANGO_HOST}/api/movies/{slug}/',
            timeout=5
        )
        
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Django API error")
        
        movie_data = response.json()
        
        # Формируем ответ
        stream_url = None
        if movie_data.get('video_file'):
            stream_url = f"/api/v1/stream/{slug}"
        elif movie_data.get('video_url'):
            stream_url = movie_data['video_url']
        
        return schemas.MovieStreamInfo(
            movie_id=movie_data['id'],
            title=movie_data['title'],
            has_video_file=bool(movie_data.get('video_file')),
            has_video_url=bool(movie_data.get('video_url')),
            stream_url=stream_url
        )
    
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Cannot connect to Django: {str(e)}")