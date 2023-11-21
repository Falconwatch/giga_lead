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
        self.n_async = self._read_conf_data()["n_async"]


    async def _base_call(self, payload: Chat):
        response = await self._giga.achat(payload)
        response_content = response.choices[0].message.content
        return response_content


    async def call(self, msg: str) -> str:
        payload = Chat(
                        messages=[
                            Messages(role=MessagesRole.SYSTEM, content = self._base_promt),
                            Messages(role=MessagesRole.USER, content=msg)],
                        temperature=0.001,
                        max_tokens=1000,
                        )
        return await self._base_call(payload)
    
    async def call_d(self, messages_t : list()) -> str:
        payload = Chat(
                        messages=messages_t,
                        temperature=0.001,
                        max_tokens=1000,
                        )
        return await self._base_call(payload)
    
    def create_messages_for_chat_json(self, msg:str, json_step_list: list):
        """ Функция создает историю чата для последующего вызов
        ARG: 
        msg - текст новости
        json_step_list - 1 вопрос 
        """

        Messeges_json = {}
        Messeges_array = list()
        Messeges_json['news_id'] = msg.news_id
        msg_text = msg.text

        for json_step in json_step_list:
            step = '1'
            if json_step['role'] == 'system':
                Messeges_array.append(Messages(role=MessagesRole.SYSTEM, content = json_step['content']))
            if json_step['role'] == 'assistant':
                Messeges_array.append(Messages(role=MessagesRole.ASSISTANT, content = json_step['content']))
            if json_step['role'] == 'user':
                Messeges_array.append(Messages(role=MessagesRole.USER,
                                                content = json_step['content'] +  ' Текст Новости: ' + msg_text))
            Messeges_json['Messeges_array'] = Messeges_array

            if json_step['role'] == 'need_next_action':
                step = json_step['Content']

            Messeges_json['step'] = step
        ### Нужно добавить еще штуку которая считает, что нужно кидать два запроса подряд
        return Messeges_json
    

    def call_dialog(self, messages: list[Messages]) -> str:
        payload = Chat(
            messages=messages,
            temperature=0.001,
            max_tokens=1000,
        )
        return self._base_call(payload)
    

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

    def _read_conf_data(self):
        #TODO: реализовать чтение данных из файла конфигурации
        try:
            config = configparser.ConfigParser()
            config.readfp(open(r'giga_lead/news_leadgen/conf/conf.cfg'))
            n_async = config.get('DEFAULT', 'n_async')
        except:
            n_async = 10
        return {"n_async": int(n_async)}


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




