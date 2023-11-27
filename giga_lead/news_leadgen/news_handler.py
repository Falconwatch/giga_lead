#from dto.newsdto import NewsDTO, ProcessedNewsDTO
from .dto.newsdto import NewsDTO, ProcessedNewsDTO
from .giga_wrappers.giga_wrappers import GigaWrapperSigma, GigaWrapperInternet, GigaWrapperAlpha
from gigachat.models import Messages, MessagesRole

from enum import Enum
from asyncio import create_task, gather
import asyncio

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
        

    async def _giga_call(self, msg: str) -> str:
        response = await self._giga_wrapper.call(msg)
        return response
    
    def get_questions_as_one_string(self) -> str:
        """Возвращает вопросы нумерованным списком"""
        return "\n".join(["{0}) {1}".format(i,q) for i,q in enumerate(self._questions)])
    
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


    async def process_news(self, one_news:NewsDTO):
        #TODO: вот тут место для экспериментов
        one_news_payload = self._get_questions_as_one_prompt(one_news.text)
        #one_news_payload = self._prepare_questions_as_many_prompts(one_news.text)
        model_response = await self._giga_call(one_news_payload)
        processing_result = ProcessedNewsDTO(news_id=one_news.news_id,
                                  processing_result=[model_response]
                                  )
        return processing_result, self.get_questions_as_one_string()
    
    async def batch_process_news(self, news: list[NewsDTO]):
        news_processing_result = list()
        step = self._giga_wrapper.n_async
        for i in range(0, len(news), step):
            tasks = list()
            for one_news in news[i:(i+step if i+step<len(news) else len(news))]:
                task = create_task(self.process_news(one_news))
                tasks.append(task)
            news_processing_result += await gather(*tasks)

        return news_processing_result
    
    def one_news(self, messages: str) -> str:
        """
        Задаем вопрос по одной ноовсти ГЧ

        ARG:
        messages: одна новость 
        
        """
        return self._giga_wrapper.call_sync(messages)
    
    def create_array_messages(self, news: NewsDTO, questions_json):
        """ Создаем массив вопросов по одной новости  
        ARG:  
        news: новость
        questions_json: список вопросов
        
        """
        mass_of = list()
        number = 1
        for iter in questions_json:
            dict_temp = self._giga_wrapper.create_messages_for_chat_json(news, iter)
            dict_temp['number'] = number
            mass_of.append(dict_temp)
            number += 1
            
        return mass_of    

    async def process_news_for_dialog(self, one_news):

        messages = one_news['Messeges_array']

        model_response = await self._giga_wrapper.call_dialog(messages)

        one_news['answer'] = model_response
        
        return one_news
    
    def preparing_news_json(self, list_news: list(), questions_json: dict) -> dict:
        """
        Функция подготавливает вопросы к вызову ГЧ. Расписана логика первого вызова, затем второго

        ARG: 
        list_news - лист новостей
        questions_json - словарик с вопросами

        """
        array_messages = list()
        for iter in list_news:
            array_messages +=  self.create_array_messages(iter, questions_json)

        first_step = [x for x in array_messages if x['step'] != '2']
        
        return first_step



    async def q(self, list_news: list(), questions_json: dict):
        """
        Вызов ГЧ

        ARG: 
        list_news - лист новостей
        questions_json - словарик с вопросами

        """
        first_step = self.preparing_news_json(list_news, questions_json)
        
        news_processing_result = list()
        step = self._giga_wrapper.n_async

        for i in range(0, len(first_step), step):
            tasks = list()
            for one_news in first_step[i:(i+step if i+step<len(first_step) else len(first_step))]:

                #messages = one_news['Messeges_array']
                
                #task = self.process_news_for_dialog(messages)
                task = self.process_news_for_dialog(one_news)

                
                tasks.append(task)
            news_processing_result += await gather(*tasks)

           


        return  news_processing_result

