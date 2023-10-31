#from dto.newsdto import NewsDTO, ProcessedNewsDTO
from .dto.newsdto import NewsDTO, ProcessedNewsDTO
from .giga_wrappers.giga_wrappers import GigaWrapperSigma, GigaWrapperInternet, GigaWrapperAlpha
from gigachat.models import Messages, MessagesRole

from enum import Enum

# class syntax
class Segments(Enum):
    ALPHA = "alpha"
    SIGMA = "sigma"
    INTERNET = "internet"

class NewsHandler():
    def __init__(self, segment:Segments = Segments.INTERNET, questions:list[str] = None):      
        if segment==Segments.ALPHA: 
            self._giga_wrapper = GigaWrapperAlpha()
        elif segment == Segments.SIGMA:
            self._giga_wrapper = GigaWrapperSigma()
        elif segment == Segments.INTERNET:
            self._giga_wrapper = GigaWrapperInternet()
        
        if questions:
            self._questions = questions
        else:
            self._questions = []
        

    def _giga_call(self, msg: str) -> str:
        response = self._giga_wrapper.call(msg)
        return response
    
    def get_questions_as_one_string(self) -> str:
        """Возвращает вопросы нумерованным списком"""
        return "\n".join(["{0}) {1}".format(i,q) for i,q in enumerate(self._questions, start=1)])
    
    def _get_questions_as_one_prompt(self, news_txt=None)->str:
        """Возвращает промпт, в котором список вопросов представлен как его часть"""
        questions_list = self.get_questions_as_one_string()
        PROMPT_TEMPLATE="""Тебе дан список вопросов и одна новость. Ответь на вопросы, при подготовке ответа не фантазируй. 
        Если не знаешь ответа, так и скажи.
        Вопросы:{0},
        Новость: {1},
        Ответы:"""
        user_prompt = PROMPT_TEMPLATE.format(questions_list, news_txt)
        return user_prompt

    
    def _prepare_questions_as_one_prompt(self, news_txt)->list[Messages]:
        user_prompt = self._get_questions_as_one_prompt(news_txt)
        messages_list = list()
        messages_list.append(
            Messages(role=MessagesRole.USER, content=user_prompt),
        )
        return messages_list
    
    def _prepare_questions_as_many_prompts(self, news_txt)->list[Messages]:
        #TODO: вовзращать список сообщений, где каждое сообщение - вопрос
        pass


    #TODO: переписать на async    
    def process_news(self, one_news:NewsDTO):

        #TODO: вот тут место для экспериментов
        one_news_payload = self._get_questions_as_one_prompt(one_news.text)
        #one_news_payload = self._prepare_questions_as_many_prompts(one_news.text)

        model_response = self._giga_call(one_news_payload)
        processing_result = ProcessedNewsDTO(news_id=one_news.news_id,
                                  processing_result=[model_response]
                                  )
        return processing_result, self.get_questions_as_one_string()

    def batch_process_news(self, news: list[NewsDTO]):
        news_processing_result = list()
        for one_news in news:
            news_processing_result.append(self.process_news(one_news))
        return news_processing_result