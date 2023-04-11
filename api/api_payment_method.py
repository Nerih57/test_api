import json
import requests


class BillingApiPaymentMethod:
    def __init__(self):
        self.base_url = "https://api-gateway.dev.idynsys.org/api/billing-settings/"

    def get_all_payments_methods(self, auth_key: json, page: str, limit: str, sort_column: str, sort_direction: str):
        headers = {'auth_key': auth_key['access_token']}
        params = {'page': page, 'limit': limit, 'sort_column': sort_column, 'sort_direction': sort_direction}
        res = requests.get(self.base_url + 'payment-methods', headers=headers, params=params)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_info_payment_method(self, auth_key: json, payment_method_id: str) -> json:
        headers = {'auth_key': auth_key['access_token']}
        res = requests.get(self.base_url + 'payment-methods/' + str(payment_method_id), headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def patch_update_payment_method(self, auth_key: json, payment_system_description: str, payment_method_id: str) \
            -> json:
        data = {
            "paymentMethodDescription": payment_system_description
        }
        headers = {'auth_key': auth_key['access_token']}
        res = requests.patch(self.base_url + 'payment-methods/' + str(payment_method_id), headers=headers, json=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
