from langchain.chat_models import GigaChat
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage

import os
from dotenv import load_dotenv

load_dotenv()
assert(os.environ["GIGACHAT_USER"])
assert(os.environ["GIGACHAT_PASSWORD"])

from gigapi import GigaAPI

giga = GigaAPI()

available_models = giga.get_models()


messages=[
            {
                "role": "system",
                "content": "Ты полезный ассистент, который умеет переводить русский на английский."
            },
            {
                "role": "user",
                "content": "Переведи это предложение. Я люблю программирование."
            },
            
        ]

response = giga.completion(messages)
print(1)
