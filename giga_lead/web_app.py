from fastapi import FastAPI, HTTPException, File, UploadFile
import uvicorn
from news_leadgen.dto.newsdto import ServiceRequestDTO, ServiceResponseDTO
from fastapi.encoders import jsonable_encoder
from news_leadgen.news_handler import NewsHandler
import pandas as pd # Новая библиотека

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


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    ''' эндпоинт который принимает на вход csv файл, проверяет корректные данные, форматирует ввод'''
    news_batch = pd.read_csv(file.file, sep = ';')

    print(news_batch.columns.values.tolist())
    # Проверяем, что колонки соответствуют названию
    mask = ['ID', 'text']
    if news_batch.columns.values.tolist() != mask:
        return HTTPException(406, detail="Wrong name of columns")

    #Переводим все колонки в стринг:

    for i in news_batch.columns:
        news_batch[i] = news_batch[i].astype(str)
            
    file.file.close()
    return HTTPException(200, detail="Upload successfully")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3003)
