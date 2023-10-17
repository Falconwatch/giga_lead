from pydantic import BaseModel

class NewsDTO(BaseModel):
    user_uid: str | None = None
    text: str 