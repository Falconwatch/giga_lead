from giga_lead.news_leadgen.dto.newsdto import NewsDTO
from giga_lead.news_leadgen.news_handler import NewsHandler

from unittest import main, IsolatedAsyncioTestCase
import pytest 

class Test(IsolatedAsyncioTestCase):
    async def test_process_one_news(self):
        nh = NewsHandler()
        one_news = NewsDTO(news_id="123",text = "текст новости")
        response = await nh.process_news(one_news)
        self.assertEqual(tuple, type(response))

    async def test_process_batch_of_news(self):
        nh = NewsHandler()
        all_news = [
            NewsDTO(news_id='aaaa', text='В Москве произошла крупная авария'),
            NewsDTO(news_id='bbbb', text='В Москве произошла крупная авария'),
            NewsDTO(news_id='cccc', text='В Москве произошла крупная авария')
        ]
        response = await nh.batch_process_news(all_news)
        self.assertEqual(list, type(response))

    async def test_base_call(self):
        nh = NewsHandler()
        response = await nh._giga_call('Мне нужен рецепт, как готовить блинчики')
        self.assertEqual(str, type(response))

@pytest.mark.asyncio
async def test_process_batch_of_news():
    nh = NewsHandler()
    all_news = [
        NewsDTO(news_id='aaaa', text='В Москве произошла крупная авария'),
        NewsDTO(news_id='bbbb', text='В Москве произошла крупная авария'),
        NewsDTO(news_id='cccc', text='В Москве произошла крупная авария')
    ]
    all_news = all_news * 10

    response = await nh.batch_process_news(all_news)

    assert len(response) == len(all_news), 'Length of Enter is not equal to Exit length'
    assert(list, type(response))
