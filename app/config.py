import weaviate
from weaviate.classes.init import AdditionalConfig, Timeout
from weaviate.classes.config import DataType
import logging

logging.basicConfig(
    filename="app.log",  # Имя файла для логов
    level=logging.INFO,  # Уровень логирования
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Подключение к локальной версии Weaviate с параметрами
client = weaviate.connect_to_local(
    host="http://weaviate",
    port=8080,
    additional_config=AdditionalConfig(timeout=Timeout(init=60, query=30, insert=60)),
    skip_init_checks=True
)

def setup_weaviate_schema():
    # Описание коллекции для видео
    collection_definition = {
        "class": "Video",
        "description": "Видео объекты с эмбеддингами",
        "vectorIndexType": "hnsw",
        "vectorIndexConfig": {
            "efConstruction": 128,
            "maxConnections": 64,
            "ef": 10
        },
        "properties": [
            {
                "name": "link",
                "description": "Ссылка на видео",
                "dataType": [DataType.TEXT],
            },
            {
                "name": "is_duplicated",
                "description": "Признак, является ли видео дубликатом",
                "dataType": [DataType.BOOL],
            },
            {
                "name": "duplicated_for",
                "description": "UUID или ссылка на видео, для которого это является дубликатом",
                "dataType": [DataType.TEXT],
            },
            {
                "name": "data",
                "description": "Эмбеддинг видео длиной 1408",
                "dataType": [DataType.NUMBER_ARRAY],
            }
        ]
    }
    logger.info(f"{client.is_ready()}")

    # Попытка создания новой коллекции, если ее нет
    try:
        existing_collections = client.collections.list_all()
        collection_names = [col for col in existing_collections] # col.name
        print(collection_names)

        if "Video" not in collection_names:
            client.collections.create_from_dict(collection_definition)
            print("Коллекция 'Video' создана!")
        else:
            print("Коллекция 'Video' уже существует.")
    except weaviate.exceptions.WeaviateQueryException as e:
        print(f"Ошибка создания коллекции: {e}")
    finally:
        logger.info(f"in finaly")
        client.close()
