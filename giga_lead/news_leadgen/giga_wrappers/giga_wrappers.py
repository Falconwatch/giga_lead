from .giga_wrapper_interface import GigaWrapperInterface
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from dotenv import load_dotenv
import os
import configparser

class BaseGigaWrapper(GigaWrapperInterface):
    def __init__(self, base_prompt="") -> None:
        super().__init__(base_prompt)
        load_dotenv()


    def _base_call(self, payload: Chat):
        response = self._giga.chat(payload)
        response_content = response.choices[0].message.content
        return response_content


    def call(self, msg: str) -> str:
        payload = Chat(
                        messages=[
                            Messages(role=MessagesRole.SYSTEM, content = self._base_promt),
                            Messages(role=MessagesRole.USER, content=msg)],
                        temperature=0.001,
                        max_tokens=1000,
                        )
        return self._base_call(payload)
    

    def call(self, messages: list[Messages]) -> str:
        payload = Chat(
            messages=messages,
            temperature=0.001,
            max_tokens=1000,
        )
        return self._base_call(payload)
    
class GigaWrapperInternet(BaseGigaWrapper):
    def __init__(self, base_prompt="") -> None:
        super().__init__(base_prompt)
        self._load_auth_data()
        self._giga = GigaChat(credentials=os.environ["AUTH"], verify_ssl_certs=False)
    
    def _load_auth_data(self):
        load_dotenv()
        assert os.environ["AUTH"]




