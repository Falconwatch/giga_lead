from pydantic import BaseModel


class NewsDTO(BaseModel):
    news_id: str
    text: str 

class ProcessedNewsDTO(BaseModel):
    news_id: str
    processing_result: list[str]

class ServiceRequestDTO(BaseModel):
    user_uid: str | None = None
    service_uid: str |None = None
    news: list[NewsDTO]

class ServiceResponseDTO(BaseModel):
    user_uid: str | None = None
    service_uid: str |None = None
    processed_news: list[ProcessedNewsDTO]