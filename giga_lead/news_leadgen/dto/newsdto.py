from pydantic import BaseModel
from typing import Optional

class NewsDTO(BaseModel):
    news_id: Optional[str] = None
    text: Optional[str] = None

class ProcessedNewsDTO(BaseModel):
    news_id: str
    processing_result: list[str]

class ServiceRequestDTO(BaseModel):
    user_uid: Optional[str] = None
    service_uid: Optional[str] = None
    news: list[NewsDTO]

class ServiceResponseDTO(BaseModel):
    user_uid: Optional[str] = None
    service_uid: Optional[str] = None
    processed_news: list[ProcessedNewsDTO]