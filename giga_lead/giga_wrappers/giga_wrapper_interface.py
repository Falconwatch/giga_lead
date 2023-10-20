from gigachat.models import Chat, Messages, MessagesRole

class GigaWrapperInterface:
    def __init__(self, base_prompt = "") -> None:
        self._base_promt = base_prompt
        
    def call(self, msg: str) -> str:
        """Простой вызов ГЧ - одно сообщение путое сообщение на вход"""
        pass

    def call_chat(self, messages: list[Messages]) -> str:
        """Вызов ГЧ с передачей истории и систем промптов"""
        pass