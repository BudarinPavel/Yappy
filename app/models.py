from typing import List

# Модель для хранения данных о видео
class VideoModel:
    def __init__(self, link: str, is_duplicated: bool, duplicated_for: str, data: List[float]):
        self.link = link
        self.is_duplicated = is_duplicated
        self.duplicated_for = duplicated_for
        self.data = data
