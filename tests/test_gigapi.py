import sys, os
sys.path.insert(0, os.path.abspath('../giga_lead'))
from giga_lead.news_leadgen.dto.newsdto import NewsDTO
from giga_lead.news_leadgen.news_handler import NewsHandler
import json

def test_process_one_news():
    nh = NewsHandler()
    result = nh.process_news("Новость")
    assert result