import json
import requests

from settings_private import base_url
from settings_private import base_url_neighbor


class BillingApiPMForApplication:
    def __init__(self):
        self.base_url = base_url
        self.base_url_neighbor = base_url_neighbor

    def get_applications(self, auth_key: json):
        headers = {'auth_key': auth_key['access_token']}
        res = requests.get(self.base_url_neighbor + 'applications', headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_all_pm_for_application(self, auth_key: json, application_id: str, page: str, limit: str, sort_column: str,
                                   sort_direction: str) -> json:
        headers = {'auth_key': auth_key['access_token']}
        params = {'application_id': application_id, 'page': page, 'limit': limit, 'sort_column': sort_column,
                  'sort_direction': sort_direction}
        res = requests.get(self.base_url + 'application-payment-methods', headers=headers, params=params)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_pm_for_application_for_add(self, auth_key: json, application_id: str, page: str, limit: str,
                                       sort_column: str, sort_direction: str) -> json:
        headers = {'auth_key': auth_key['access_token']}
        params = {'application_id': application_id, 'page': page, 'limit': limit, 'sort_column': sort_column,
                  'sort_direction': sort_direction}
        res = requests.get(self.base_url + 'application-payment-methods/available-to-add', headers=headers,
                           params=params)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_pm_for_application(self, auth_key: json, application_payment_method_id: str) -> json:
        headers = {'auth_key': auth_key['access_token']}
        res = requests.get(self.base_url + 'application-payment-methods/' + application_payment_method_id,
                           headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_add_pm_for_application(self, auth_key: json, payment_method_id: str, application_id: str) -> json:
        data = {
            "paymentMethodId": payment_method_id,
            "applicationId": application_id
        }
        headers = {'auth_key': auth_key['access_token']}
        res = requests.post(self.base_url + 'application-payment-methods', headers=headers, json=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def put_update_pm_for_applications(self, auth_key: json, application_id: str, active: bool) -> json:
        data = {
            "isActive": active
        }
        headers = {'auth_key': auth_key['access_token']}
        res = requests.put(self.base_url + 'application-payment-methods/' + str(application_id), headers=headers,
                           json=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def patch_update_activation_pm_for_applications(self, auth_key: json, application_id: str, active: bool) -> json:
        data = {
            "isActive": active
        }
        headers = {'auth_key': auth_key['access_token']}
        res = requests.patch(self.base_url + 'application-payment-methods/' + str(application_id) + '/activation',
                             headers=headers, json=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
