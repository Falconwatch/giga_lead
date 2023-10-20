from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
import os
from dto.newsdto import NewsDTO, ProcessedNewsDTO
from giga_wrappers.giga_wrappers import GigaWrapperSigma, GigaWrapperInternet


class NewsHandler():
    def __init__(self):       
        self._giga_wrapper = GigaWrapperInternet()
        

    def _giga_call(self, msg: str) -> str:
        response = self._giga_wrapper.call(msg)
        return response
        #TODO: удалить после отладки
        return "model response"
        
        #TODO: реализовать логику вызова нейронки. Потенциально два варианта: сигма и внешний(?)
        #тут писать логику обработки одной новости
        payload = Chat(
            messages=[
                Messages(
                    role=MessagesRole.SYSTEM,
                    #TODO: вытащить систем промпт в конфиг
                    content="Ты эксперт банковского сектора. На соновании данной новости отвечай на заданные вопросы. Не фантазируй, используй только данную тебе информацию"
                )
            ],
            temperature=0.001,
            max_tokens=1000,
        )

        response = self._giga.chat(payload)



        interesting_questions="""О каких компаниях идёт речь в новости? 
            Предположи какие банковские продукты могут быть инетресны компаниям в новости?"""
        user_input = one_news + interesting_questions

        payload.messages.append(Messages(role=MessagesRole.USER, content=user_input))

        

    #TODO: переписать на async    
    def process_news(self, one_news:NewsDTO):
        model_response = self._giga_call(one_news.text)
        result = ProcessedNewsDTO(news_id=one_news.news_id,
                                  processing_result=[model_response]
                                  )
        return result

    def batch_process_news(self, news: list[NewsDTO]):
        news_processing_result = list()
        for one_news in news:
            news_processing_result.append(self.process_news(one_news))
        return news_processing_result