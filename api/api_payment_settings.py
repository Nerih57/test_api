import json
import requests

from settings_private import base_url


class BillingApiPaymentSettings:
    def __init__(self):
        self.base_url = base_url

    def get_all_payments_system(self, auth_key: json, page: str, limit: str, sort_column: str, sort_direction: str):
        headers = {'auth_key': auth_key['access_token']}
        params = {'page': page, 'limit': limit, 'sort_column': sort_column, 'sort_direction': sort_direction}
        res = requests.get(self.base_url + 'payment-systems', headers=headers, params=params)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_info_payment_system(self, auth_key: json, payment_system_id: str) -> json:
        headers = {'auth_key': auth_key['access_token']}
        res = requests.get(self.base_url + 'payment-systems/' + str(payment_system_id), headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def patch_update_payment_system(self, auth_key: json, payment_system_name: str, payment_system_description: str,
                                    active: bool, payment_system_id: str) -> json:
        data = {
            "paymentSystemName": payment_system_name,
            "paymentSystemDescription": payment_system_description,
            "isActive": active
        }
        headers = {'auth_key': auth_key['access_token']}
        res = requests.patch(self.base_url + 'payment-systems/' + str(payment_system_id), headers=headers, json=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_all_payments_methods_for_ps(self, auth_key: json, page: str, limit: str, sort_column: str,
                                        sort_direction: str, payment_system_id: str):
        headers = {'auth_key': auth_key['access_token']}
        params = {'page': page, 'limit': limit, 'sort_column': sort_column, 'sort_direction': sort_direction}
        res = requests.get(self.base_url + 'payment-systems/' + payment_system_id + '/payment-methods',
                           headers=headers, params=params)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_filter_payments_methods_for_ps(self, auth_key: json, page: str, limit: str, active: str,
                                           payment_system_id: str):
        headers = {'auth_key': auth_key['access_token']}
        params = {'page': page, 'limit': limit, 'is_active': active}
        res = requests.get(self.base_url + 'payment-systems/' + payment_system_id + '/payment-methods',
                           headers=headers, params=params)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_info_payment_method(self, auth_key: json, payment_method_id: str) -> json:
        headers = {'auth_key': auth_key['access_token']}
        res = requests.get(self.base_url + 'payment-system-methods/' + str(payment_method_id), headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def patch_update_payment_method(self, auth_key: json, active: bool, payment_method_id: str) -> json:
        data = {
            "isActive": active
        }
        headers = {'auth_key': auth_key['access_token']}
        res = requests.patch(self.base_url + 'payment-system-methods/' + str(payment_method_id),
                             headers=headers, json=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_all_organization_for_ps(self, auth_key: json, page: str, limit: str, sort_column: str,
                                    sort_direction: str, payment_system_id: str):
        headers = {'auth_key': auth_key['access_token']}
        params = {'page': page, 'limit': limit, 'sort_column': sort_column, 'sort_direction': sort_direction}
        res = requests.get(self.base_url + 'payment-systems/' + payment_system_id + '/organizations',
                           headers=headers, params=params)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_filter_organization_for_ps(self, auth_key: json, page: str, limit: str, active: str,
                                       organization_type, payment_system_id: str):
        headers = {'auth_key': auth_key['access_token']}
        params = {'page': page, 'limit': limit, 'is_active': active, 'organization_type': organization_type}
        res = requests.get(self.base_url + 'payment-systems/' + payment_system_id + '/organizations',
                           headers=headers, params=params)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def put_update_active_organization(self, auth_key: json, active: bool, payment_system_id: str,
                                       organization_id: str) -> json:
        data = {
            "isPaymentSystemActiveForOrganization": active
        }
        headers = {'auth_key': auth_key['access_token']}
        res = requests.put(self.base_url + 'payment-systems/' + str(payment_system_id) + '/organizations/' +
                           str(organization_id), headers=headers, json=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_active_organization_for_ps(self, auth_key: json, payment_system_id: str) -> json:
        headers = {'auth_key': auth_key['access_token']}
        res = requests.get(self.base_url + 'payment-systems/' + str(payment_system_id) + '/active-organizations',
                           headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_all_ps_for_organization(self, auth_key: json, page: str, limit: str, sort_column: str,
                                    sort_direction: str, organization_id: str):
        headers = {'auth_key': auth_key['access_token']}
        params = {'page': page, 'limit': limit, 'sort_column': sort_column, 'sort_direction': sort_direction}
        res = requests.get(self.base_url + 'organization/' + organization_id + '/payment-systems',
                           headers=headers, params=params)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
