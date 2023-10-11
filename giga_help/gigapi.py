import requests
import json
import datetime
from dotenv import load_dotenv
import os
import uuid

class GigaAPI():
    def __init__(self) -> None:
        self._auth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        self._expires_at = None
        self._token = None
        load_dotenv()
        self._secret = os.environ["SECRET"]

    def refresh_token(self):
        payload = 'scope=GIGACHAT_API_CORP'
        headers = {
        'Authorization': 'Bearer {0}'.format(self._secret),
        'RqUID': '{0}'.format(str(uuid.uuid4())),
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", self._auth_url, headers=headers, data=payload, verify=False)
        body = json.loads(response.content)        
        access_token = body["access_token"]
        expires_at = body["expires_at"]

        self._token = access_token
        self._expires_at = expires_at

    def get_token(self):
        self.validate_token()
        return self._token
    
    def is_token_expired(self):
        if self._expires_at:
            return self._expires_at < datetime.datetime.now().timestamp()*1000
        else:
            return True
        
    def validate_token(self):
        if self.is_token_expired():
            self.refresh_token()
    
    def token_decorator(func): 
        def inner1(*args): 
            args[0].validate_token()
            return func(*args)
        return inner1 
        
    @token_decorator  
    def get_models(self):
        url = "https://gigachat.devices.sberbank.ru/api/v1/models"
        payload = {}
        headers = {
            'Authorization': 'Bearer {0}'.format(self._token)
        }
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        result = json.loads(response.content)
        return result

    @token_decorator    
    def completion(self, messages = [
            {
                "role": "user",
                "content": "Когда уже ИИ захватит этот мир?"
            }
        ]):

        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        payload = json.dumps({
        "model": "GigaChat:latest",
        "messages": messages,
        "temperature": 0.9
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {0}'.format(self._token)
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        return response.text



        

