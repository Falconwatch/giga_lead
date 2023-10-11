from giga_help.gigapi import GigaAPI

def test_get_token():
    ga = GigaAPI()
    token = ga.get_token()
    assert token

def test_get_models():
    ga = GigaAPI()
    models = ga.get_models()
    assert len(models["data"])>0


