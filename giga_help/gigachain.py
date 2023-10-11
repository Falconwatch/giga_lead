import gigachain
from gigapi import GigaAPI


ga = GigaAPI()
tmp = ga.get_token()
models = ga.get_models()

from langchain.chat_models.gigachat import GigaChat
giga = GigaChat(profanity=False, 
                ssl_verify=False,
                verify_ssl_certs=False,
                credentials=tmp)

from langchain.chains import ConversationalRetrievalChain

qa = ConversationalRetrievalChain.from_llm(giga, retriever=retriever)


print(models)
