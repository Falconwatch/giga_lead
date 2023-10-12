from news_handler import NewsHandler


nh = NewsHandler()

#пример на одной новости
one_n_response = nh.process_news("Газром заявил о намерении инвестировать в переработку газа")

news = ["Новость 1",
        "Новость 2"]
batch_n_response = nh.batch_process_news(news)

print(1)

