from pydantic import BaseModel, HttpUrl

# Запрос на проверку видео
class VideoLinkRequest(BaseModel):
    link: str

# Ответ с результатом дубликата
class VideoLinkResponse(BaseModel):
    is_duplicate: bool
    duplicate_for: str
