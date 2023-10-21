from fastapi import FastAPI, HTTPException
import uvicorn
from news_leadgen.dto.newsdto import ServiceRequestDTO, ServiceResponseDTO
from fastapi.encoders import jsonable_encoder
from news_leadgen.news_handler import NewsHandler

app = FastAPI()
nh = NewsHandler()

#TODO: Убрать, использовалось для дебага
nh._giga_call("Моё сообщение")


@app.get("/ping")
async def ping():
    return "pong"


@app.post("/news/batch")
async def process_batch_news(batch_news: ServiceRequestDTO) -> ServiceResponseDTO:
    batch_news_response = [nh.process_news(one_news.text) for one_news in batch_news.news]
    if batch_news_response & len(batch_news_response):
        return jsonable_encoder(batch_news_response)
    return HTTPException(400, detail="Something went wrong")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3003)