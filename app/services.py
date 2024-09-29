import numpy as np
from app.config import client
from app.models import VideoModel
from typing import List
import uuid


# Генерация случайного эмбеддинга (пока заглушка)
def generate_random_embedding(length=1408) -> List[float]:
    return np.random.rand(length).tolist()

# Поиск дубликата в Weaviate
def search_duplicate_in_weaviate(new_embedding: List[float], cosine_threshold: float):
    result = client.query.get("Video", ["link", "is_duplicated", "duplicated_for"]) \
        .with_near_vector({"vector": new_embedding, "distance": cosine_threshold}) \
        .do()
    return result

# Добавление нового видео в Weaviate
def add_video_to_weaviate(link: str, is_duplicated: bool, duplicated_for: str, embedding: List[float]):
    data_object = VideoModel(link, is_duplicated, duplicated_for, embedding)
    video_uuid = str(uuid.uuid4())
    client.data_object.create(
        class_name="Video",
        data_object=data_object.__dict__,
        uuid=video_uuid
    )
