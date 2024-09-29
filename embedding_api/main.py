from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI()

class TextInput(BaseModel):
    text: str

# Длина эмбеддинга, которую будет использовать Weaviate (например, 1408)
EMBEDDING_LENGTH = 1408

# Маршрут для генерации эмбеддинга
@app.post("/embed")
async def embed_text(input: TextInput):
    # Возвращаем случайный эмбеддинг
    embedding = np.random.rand(EMBEDDING_LENGTH).tolist()
    return {"embedding": embedding}

# Маршрут для проверки готовности сервиса
@app.get("/.well-known/ready")
async def ready():
    return {"status": "ok"}

# Маршрут для проверки готовности Weaviate на уровне /embed/.well-known/ready
@app.get("/embed/.well-known/ready")
async def embed_ready():
    return {"status": "ok"}

# Маршрут для предоставления метаинформации
@app.get("/embed/meta")
async def embed_meta():
    return {
        "name": "Embedding API",
        "version": "1.0.0",
        "description": "API для получения эмбеддингов видео"
    }
