from fastapi import FastAPI
#from app.routers import video
from app.config import setup_weaviate_schema


from app.routers.video import fetch_embedding_from_api
from app.schemas import VideoLinkRequest, VideoLinkResponse
from app.services import search_duplicate_in_weaviate, add_video_to_weaviate
import logging
from fastapi import APIRouter, HTTPException
import httpx  # Импортируем httpx для отправки запросов

logging.basicConfig(
    filename="app.log",  # Имя файла для логов
    level=logging.INFO,  # Уровень логирования
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

COSINE_THRESHOLD = 0.75

app = FastAPI()

# Инициализация схемы в Weaviate
setup_weaviate_schema()
logger.info(f"Start")
# Подключаем роутеры
#app.include_router(video.router)


@app.post("/check-video-duplicate", response_model=VideoLinkResponse)
async def process_video(video_link: VideoLinkRequest):
    print('test')
    logger.info(f"Starting to process video: {video_link.link}")
    try:
        logger.info(f"Received request for video: {video_link.link}")

        # Запрос на API для получения эмбеддинга
        new_embedding = await fetch_embedding_from_api(video_link.link)
        logger.debug(f"Generated embedding: {new_embedding[:10]}...")  # Логируем первые 10 значений для краткости

        # Поиск дубликата в Weaviate
        search_result = search_duplicate_in_weaviate(new_embedding, COSINE_THRESHOLD)
        logger.info(f"Search result: {search_result}")

        is_duplicate = False
        duplicate_for = ""

        if len(search_result["data"]["Get"]["Video"]) > 0:
            closest_match = search_result["data"]["Get"]["Video"][0]
            is_duplicate = True
            duplicate_for = closest_match["link"]
            logger.info(f"Duplicate found for video: {duplicate_for}")

        # Добавляем видео в Weaviate
        add_video_to_weaviate(video_link.link, is_duplicate, duplicate_for, new_embedding)
        logger.info(f"Video {video_link.link} added to Weaviate.")

        return VideoLinkResponse(is_duplicate=is_duplicate, duplicate_for=duplicate_for if is_duplicate else "")
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Запуск FastAPI приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=80)
