from news_handler import NewsHandler
from fastapi import FastAPI, HTTPException
import uvicorn
from dto.newsdto import NewsDTO, ServiceResponseDTO
from fastapi.encoders import jsonable_encoder


app = FastAPI()
nh = NewsHandler()

@app.get("/ping")
async def ping():
    return "pong"


@app.post("/news/batch")
async def process_batch_news(batch_news: ServiceResponseDTO):
    batch_news_response = [nh.process_news(one_news.text) for one_news in batch_news.news]
    if batch_news_response & len(batch_news_response):
        return jsonable_encoder(batch_news_response)
    return HTTPException(400, detail="Something went wrong")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3003)