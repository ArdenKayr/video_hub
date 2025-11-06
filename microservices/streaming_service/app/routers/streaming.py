from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pathlib import Path
import os
import re
from .. import models
from ..database import get_db
from ..config import settings

router = APIRouter(prefix="/stream", tags=["streaming"])

async def ranged_stream(file_path: str, start: int, end: int, chunk_size: int = 1024 * 1024):
    """Генератор для потокового видео с поддержкой Range"""
    with open(file_path, 'rb') as video:
        video.seek(start)
        remaining = end - start + 1
        
        while remaining > 0:
            chunk = min(chunk_size, remaining)
            data = video.read(chunk)
            if not data:
                break
            remaining -= len(data)
            yield data

@router.get("/{slug}")
async def stream_video(
    slug: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Стриминг видео с поддержкой Range запросов"""
    
    # Получаем фильм из БД
    movie = db.query(models.Movie).filter(
        models.Movie.slug == slug
    ).first()
    
    if not movie or not movie.video_file:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Полный путь к видео
    video_path = Path(settings.MEDIA_ROOT) / movie.video_file
    
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video file not found")
    
    # Получаем размер файла
    file_size = os.path.getsize(video_path)
    
    # Обработка Range заголовка
    range_header = request.headers.get('range')
    
    if range_header:
        # Парсим Range заголовок
        range_match = re.search(r'bytes=(\d+)-(\d*)', range_header)
        if range_match:
            start = int(range_match.group(1))
            end = int(range_match.group(2)) if range_match.group(2) else file_size - 1
            
            # Создаем StreamingResponse с статусом 206
            headers = {
                'Content-Range': f'bytes {start}-{end}/{file_size}',
                'Accept-Ranges': 'bytes',
                'Content-Length': str(end - start + 1),
                'Content-Type': 'video/mp4',
            }
            
            return StreamingResponse(
                ranged_stream(str(video_path), start, end),
                status_code=206,
                headers=headers,
                media_type='video/mp4'
            )
    
    # Если нет Range заголовка - полный файл
    def full_stream():
        with open(video_path, 'rb') as video:
            while chunk := video.read(1024 * 1024):
                yield chunk
    
    headers = {
        'Accept-Ranges': 'bytes',
        'Content-Length': str(file_size),
        'Content-Type': 'video/mp4',
    }
    
    return StreamingResponse(
        full_stream(),
        headers=headers,
        media_type='video/mp4'
    )