#from dto.newsdto import NewsDTO, ProcessedNewsDTO
from .dto.newsdto import NewsDTO, ProcessedNewsDTO
from .giga_wrappers.giga_wrappers import GigaWrapperSigma, GigaWrapperInternet, GigaWrapperAlpha

from enum import Enum

# class syntax
class Segments(Enum):
    ALPHA = "alpha"
    SIGMA = "sigma"
    INTERNET = "internet"

class NewsHandler():
    def __init__(self, segment:Segments = Segments.INTERNET):      
        if segment==Segments.ALPHA: 
            self._giga_wrapper = GigaWrapperAlpha()
        elif segment == Segments.SIGMA:
            self._giga_wrapper = GigaWrapperSigma()
        elif segment == Segments.INTERNET:
            self._giga_wrapper = GigaWrapperInternet()
        

    def _giga_call(self, msg: str) -> str:
        response = self._giga_wrapper.call(msg)
        return response
        

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