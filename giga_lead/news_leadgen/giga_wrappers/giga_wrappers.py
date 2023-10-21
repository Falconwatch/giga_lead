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

    def call(self, msg: str) -> str:
        payload = Chat(
                        messages=[
                            Messages(role=MessagesRole.SYSTEM, content = self._base_promt),
                            Messages(role=MessagesRole.USER, content=msg)],
                        temperature=0.001,
                        max_tokens=1000,
                        )
        response = self._giga.chat(payload)
        response_content = response.choices[0].message.content
        return response_content
    
    def _read_cert_data(self):
        #TODO: реализовать чтение данных из файла конфигурации
        config = configparser.ConfigParser()
        config.readfp(open(r'certs/certs.cfg'))
        ca_bundle_file = config.get('CERTS', 'ca_bundle_file')
        cert_file = config.get('CERTS', 'cert_file')
        key_file = config.get('CERTS', 'key_file')
        key_file_password = config.get('CERTS', 'key_file_password')
        return {"ca_bundle_file": ca_bundle_file,
                "cert_file": cert_file,
                "key_file": key_file,
                "key_file_password": key_file_password}


class GigaWrapperSigma(BaseGigaWrapper):
    def __init__(self, base_prompt="") -> None:
        super().__init__(base_prompt)
        self._giga = GigaChat(
            base_url="https://gigachat.devices.sberbank.ru/api/v1",
            verify_ssl_certs=False,
            **self._read_cert_data()
        )


class GigaWrapperAlpha(BaseGigaWrapper):
    def __init__(self) -> None:
        super().__init__()
        self._giga = GigaChat(
            base_url="https://gigachat.devices.sberbank.ru/api/v1",
            verify_ssl_certs=False,
            **self._read_cert_data()
        )


class GigaWrapperInternet(BaseGigaWrapper):
    def __init__(self, base_prompt="") -> None:
        super().__init__(base_prompt)
        self._load_auth_data()
        self._giga = GigaChat(credentials=os.environ["AUTH"], verify_ssl_certs=False)
    
    def _load_auth_data(self):
        load_dotenv()
        assert os.environ["AUTH"]




