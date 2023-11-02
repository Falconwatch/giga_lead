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


@app.post("/news/batch") # Это эндпоинт
async def process_batch_news(batch_news: ServiceRequestDTO) -> ServiceResponseDTO:
    batch_news_response = [nh.process_news(one_news.text) for one_news in batch_news.news]
    if batch_news_response & len(batch_news_response):
        return jsonable_encoder(batch_news_response)
    return HTTPException(400, detail="Something went wrong")

@app.post("/file/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    from news_leadgen.news_handler import NewsHandler
    
    news_batch = pd.read_excel(file.file)[:3]
    news_processing_batch = nh.batch_process_news(news_batch)
    npb_list = list()
    for npr in news_processing_batch:
        npb_list.append((npr[1], npr[0].news_id, npr[0].processing_result))

    responses = pd.DataFrame(data=npb_list, columns=["Заданные вопросы", "ID новости", "Ответы на вопросы"])
    
    file.file.close()
    return file.filename, responses.head()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3003)
