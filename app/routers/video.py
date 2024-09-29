from fastapi import APIRouter, HTTPException
from app.schemas import VideoLinkRequest, VideoLinkResponse
from app.services import search_duplicate_in_weaviate, add_video_to_weaviate
import logging
import httpx  # Импортируем httpx для отправки запросов

logging.basicConfig(
    filename="app.log",  # Имя файла для логов
    level=logging.INFO,  # Уровень логирования
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

#router = APIRouter()

COSINE_THRESHOLD = 0.75

# Функция для обращения к API заглушки для генерации эмбеддинга
async def fetch_embedding_from_api(video_link: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8081/embed",  # Адрес вашего API для заглушки
                json={"text": video_link}
            )
            response.raise_for_status()
            embedding_data = response.json()
            return embedding_data["embedding"]
    except httpx.RequestError as exc:
        logger.error(f"An error occurred while requesting embedding: {exc}")
        raise HTTPException(status_code=500, detail="Error fetching embedding from API")

# Маршрут для проверки видео

