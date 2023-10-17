from pydantic import BaseModel


class NewsDTO(BaseModel):
    news_uid: str
    text: str 

class ServiceResponseDTO(BaseModel):
    user_uid: str | None = None
    service_uid: str |None = None
    news: list[NewsDTO]