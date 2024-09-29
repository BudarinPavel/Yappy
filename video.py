import weaviate

# Подключение к Weaviate
client = weaviate.Client("http://localhost:8080")  # Замените на URL вашего Weaviate-инстанса

# Описание схемы
class_obj = {
    "class": "Video",  # Имя класса
    "description": "Видео объекты с эмбеддингами",  # Описание класса
    "properties": [
        {
            "name": "link",
            "description": "Ссылка на видео в хранилище",
            "dataType": ["string"],  # Ссылка как строка
        },
        {
            "name": "is_duplicated",
            "description": "Признак, является ли видео дубликатом",
            "dataType": ["boolean"],  # Булевое значение
        },
        {
            "name": "duplicated_for",
            "description": "UUID видео, для которого это является дубликатом",
            "dataType": ["string"],  # UUID как строка
        },
        {
            "name": "data",
            "description": "Эмбеддинг видео длиной 1408",
            "dataType": ["number[]"],  # Массив чисел (вектор эмбеддингов)
        }
    ]
}

# Проверяем, существует ли уже этот класс, если нет — создаем его
if not client.schema.contains({"class": "Video"}):
    client.schema.create_class(class_obj)
    print("Схема создана")
else:
    print("Класс 'Video' уже существует")
