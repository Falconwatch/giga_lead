from ..giga_lead.dto.newsdto import NewsDTO
from ..news_leadgen.news_handler import NewsHandler

def test_process_one_news():
    nh = NewsHandler()
    one_news = NewsDTO()
    one_news.news_id = "123"
    one_news.text = "текст новости"

    response = nh.process_news(one_news)
    assert response