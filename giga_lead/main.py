from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

import os
from dotenv import load_dotenv
load_dotenv()
assert(os.environ["SECRET"])


payload = Chat(
    messages=[
        Messages(
            role=MessagesRole.SYSTEM,
            content="Ты эксперт банковского сектора. На соновании данной новости отвечай на заданные вопросы. Не фантазируй, используй только данную тебе информацию"
        )
    ],
    temperature=0.001,
    max_tokens=1000,
)

one_news = "Газпром решил инвестировать в газоперерабатывающий завод"
interesting_questions="""О каких компаниях идёт речь в новости? 
Предположи какие банковские продукты могут быть инетресны компаниям в новости?"""

user_input = one_news + interesting_questions

with GigaChat(credentials=os.environ["SECRET"], verify_ssl_certs=False) as giga:
        payload.messages.append(Messages(role=MessagesRole.USER, content=user_input))
        response = giga.chat(payload)
print("Bot: ", response.choices[0].message.content)

