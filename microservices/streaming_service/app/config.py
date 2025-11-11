from pydantic_settings import BaseSettings
import re
from typing import Any
from pathlib import Path
import os

class Settings(BaseSettings):
    # --------------------- DATABASE ---------------------
    # SQLite3: файл videohub.db в корне проекта
    DATABASE_URL: str = "sqlite:///videohub.db"

    # --------------------- MEDIA ---------------------
    MEDIA_ROOT: str = "media"  # относительный путь от корня проекта

    # --------------------- API ---------------------
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "VideoHub Streaming Service"

    # --------------------- CORS ---------------------
    DJANGO_HOST: str = "http://localhost:8000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    # ---------- ОЧИСТКА СКРЫТЫХ СИМВОЛОВ (от 0xC2 0xA0 и др.) ----------
    def _clean_string(self, value: str) -> str:
        if not isinstance(value, str):
            return value
        value = value.replace("\u00a0", " ")                    # неразрывный пробел → обычный
        value = re.sub(r'[\u200B\u2060\uFEFF\u00AD\u200C\u200D\u200E\u200F\u061C]', '', value)  # zero-width &zwj;
        value = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', value)  # control chars
        value = re.sub(r'\s+', ' ', value).strip()
        return value

    def model_post_init(self, __context: Any) -> None:
        # Чистим все строковые поля
        for field_name, field_value in self.__dict__.items():
            if isinstance(field_value, str):
                cleaned = self._clean_string(field_value)
                setattr(self, field_name, cleaned)

        # ----------------- АВТОМАТИЧЕСКОЕ СОЗДАНИЕ ПАПОК -----------------
        # Делаем MEDIA_ROOT абсолютным путём и создаём папку, если нет
        media_path = Path(self.MEDIA_ROOT)
        if not media_path.is_absolute():
            # Относительно текущего файла config.py
            base_dir = Path(__file__).parent
            media_path = base_dir / media_path
        self.MEDIA_ROOT = str(media_path.resolve())

        # Создаём папку media, если её нет
        os.makedirs(self.MEDIA_ROOT, exist_ok=True)

        # Переопределяем DATABASE_URL как абсолютный путь к БД
        db_path = Path(__file__).parent / "videohub.db"
        self.DATABASE_URL = f"sqlite:///{db_path.resolve()}"

        # (Опционально) можно вывести в консоль для отладки
        # print(f"[Settings] DATABASE_URL → {self.DATABASE_URL}")
        # print(f"[Settings] MEDIA_ROOT   → {self.MEDIA_ROOT}")


# Создаём экземпляр — вся магия (очистка + создание папок) происходит автоматически
settings = Settings()