
from news_leadgen.dto.newsdto import ServiceRequestDTO, ServiceResponseDTO
from news_leadgen.news_handler import NewsHandler
from news_leadgen.giga_wrappers.giga_wrappers import GigaWrapperInternet
from gigachat.models.messages_role import MessagesRole
from gigachat.models import Messages

gw=GigaWrapperInternet()

messages=[
    Messages(role=MessagesRole.SYSTEM, content = "Ты бот-помощник. Отвечай не фантазируя"),
    Messages(role=MessagesRole.USER, content= "Что ты умеешь?"),
    Messages(role=MessagesRole.ASSISTANT, content = "Я умею всё, кроме фантазирования"),
    Messages(role=MessagesRole.USER, content= "Как тебя зовут?"),
]

tmp = gw.call_dialog(messages)
print(tmp)
