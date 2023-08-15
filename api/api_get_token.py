import json
import requests

from settings_private import base_url_for_token


class BillingApiToken:
    def __init__(self):
        self.base_url_for_token = base_url_for_token

    def get_api_key(self, data: dict):
        data = data
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        res = requests.post(self.base_url_for_token + 'realms/b2b/protocol/openid-connect/token', headers=headers,
                            data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
