from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
import os


class NewsHandler():
    def __init__(self):
        load_dotenv()
        try:
            assert(os.environ["SECRET"])
        except:
            raise BaseException("не удалось считать secret")
        
        self._giga = GigaChat(credentials=os.environ["SECRET"], verify_ssl_certs=False)
        
    def process_news(self, one_news):
        one_news_processing_result = ""
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

        interesting_questions="""О каких компаниях идёт речь в новости? 
            Предположи какие банковские продукты могут быть инетресны компаниям в новости?"""
        user_input = one_news + interesting_questions

        payload.messages.append(Messages(role=MessagesRole.USER, content=user_input))
        response = self._giga.chat(payload)
        one_news_processing_result = response.choices[0].message.content

        return one_news_processing_result

    def batch_process_news(self, news):
        news_processing_result = list()
        for one_news in news:
            news_processing_result.append(self.process_news(one_news))
        return news_processing_result