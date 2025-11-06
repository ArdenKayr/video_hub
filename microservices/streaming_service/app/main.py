from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import movies, streaming

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.DJANGO_HOST, "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(movies.router, prefix=settings.API_V1_PREFIX)
app.include_router(streaming.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
async def root():
    return {
        "message": "VideoHub Streaming Service",
        "docs": f"{settings.API_V1_PREFIX}/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}