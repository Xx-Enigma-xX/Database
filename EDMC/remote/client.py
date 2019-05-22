import requests
import json

class RemoteDatabase:
    def __init__(self, url, token):
        headers = {"token": token}
        try:
            response = requests.get(url, headers=headers)
        except:
            response = requests.get(url, headers=headers, verify=False)
        if not response.status_code == 200:
            raise Exception('Status code isn\'t 200')
        response.raise_for_status
        jsonResponse = json.loads(response.content)
        if not jsonResponse["type"] == "Enigma Database":
            raise Exception('Incorrect Database')
        self.url = url
