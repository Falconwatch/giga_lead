from news_leadgen.news_handler import NewsHandler

def test_process_one_news():
    nh = NewsHandler()
    result = nh.process_news("Новость")
    assert result