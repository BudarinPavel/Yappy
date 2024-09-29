from fastapi import FastAPI
from pydantic import BaseModel

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Uuid, Boolean, Text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

import json
import uuid

# from typing import Any

app = FastAPI()

# Создать базу данных для хранения обработанных видео и признаков
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# создание движка
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

class Base(DeclarativeBase): pass

class Video(Base):
    __tablename__ = "video"

    id = Column(Uuid, primary_key=True, index=True)
    link = Column(String)
    is_duplicated = Column(Boolean)
    duplicated_for = Column(Uuid)
    data = Column(Text)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()

tom = Video(id = uuid.uuid4(), link = "Tom.mp4", is_duplicated = False, duplicated_for = uuid.uuid4(), data = "")
db.add(tom)  # добавляем в бд
db.commit()  # сохраняем изменения

print(tom.id)  # можно получить установленный id

class VideoLinkRequest(BaseModel):
    link: str

class VideoLinkResponse(BaseModel):
    is_duplicate: bool
    duplicate_for: str

@app.post("/check-video-duplicate", response_model=VideoLinkResponse)
async def process_video(video_link: VideoLinkRequest):
    video_id = str(uuid.uuid4())

    # загрузить файл, отдать на вход в мл

    # выгрузить данные из бд для алгоритма определения дубликата

    # запись в бд нового видео

    # генерация response

    is_duplicate = False
    duplicate_for = ""
    return VideoLinkResponse(is_duplicate=is_duplicate, duplicate_for=duplicate_for)

    # Ищем дубликат в "базе данных"
    # if video_link.link in video_database:
    #     # Видео найдено, возвращаем дубликат
    #     return VideoLinkResponse(
    #         is_duplicate=True,
    #         duplicate_for=video_database[video_link.link]
    #     )
    # else:
    #     # Если видео не найдено, генерируем новый UUID для него
    #     return VideoLinkResponse(
    #         is_duplicate=False,
    #         duplicate_for=uuid4()  # Новый случайный идентификатор, если нет дубликата
    #     )

# 1. научиться писать в бд
# 2. решить как искать дубли по прешедшему видео
# 3. векторная бд?
# 4. бейзлайн два вектора видео

