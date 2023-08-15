import json
import requests

from settings_private import base_url


class BillingApiPaymentSettingsAccounts:
    def __init__(self):
        self.base_url = base_url

    def get_all_payments_system_accounts(self, auth_key: json, page: str, limit: str, sort_column: str,
                                         sort_direction: str):
        headers = {'auth_key': auth_key['access_token']}
        params = {'page': page, 'limit': limit, 'sort_column': sort_column, 'sort_direction': sort_direction}
        res = requests.get(self.base_url + 'payment-systems-accounts', headers=headers, params=params)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_info_payment_system_account(self, auth_key: json, psa_id: str) -> json:
        headers = {'auth_key': auth_key['access_token']}
        res = requests.get(self.base_url + 'payment-systems-accounts/' + str(psa_id), headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_add_ps_account(self, auth_key: json, ps_name: str, ps_description: str,
                            organization_id: str, payment_system_id: str) -> json:
        data = {
            "paymentSystemAccountName": ps_name,
            "paymentSystemAccountDescription": ps_description,
            "organizationId": organization_id,
            "paymentSystemId": payment_system_id
        }
        headers = {'auth_key': auth_key['access_token']}
        res = requests.post(self.base_url + 'payment-systems-accounts', headers=headers, json=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def patch_update_ps_account(self, auth_key: json, ps_name: str, ps_description: str, organization_id: str,
                                psa_id: str) -> json:
        data = {
            "paymentSystemAccountName": ps_name,
            "paymentSystemAccountDescription": ps_description,
            "organizationId": organization_id
        }
        headers = {'auth_key': auth_key['access_token']}
        res = requests.patch(self.base_url + 'payment-systems-accounts/' + str(psa_id), headers=headers, json=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_add_currency_for_ps_account(self, auth_key: json, currency_name: str, currency_description: str,
                                         currency_iso: str, psa_id: str) -> json:
        data = {
            "currencyAccountName": currency_name,
            "currencyAccountDescription": currency_description,
            "currencyIsoCode": currency_iso
        }
        headers = {'auth_key': auth_key['access_token']}
        res = requests.post(self.base_url + 'payment-systems-accounts/' + str(psa_id) + '/currency-accounts',
                            headers=headers, json=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_all_currency_accounts_for_psa(self, auth_key: json, page: str, limit: str, sort_column: str,
                                          sort_direction: str, psa_id: str):
        headers = {'auth_key': auth_key['access_token']}
        params = {'page': page, 'limit': limit, 'sort_column': sort_column, 'sort_direction': sort_direction}
        res = requests.get(self.base_url + 'payment-systems-accounts/' + str(psa_id) + '/currency-accounts',
                           headers=headers, params=params)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_info_currency_account_for_psa(self, auth_key: json, currency_id: str) -> json:
        headers = {'auth_key': auth_key['access_token']}
        res = requests.get(self.base_url + 'payment-systems-accounts/currency-accounts/' + str(currency_id),
                           headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def patch_update_currency_account_fore_psa(self, auth_key: json, currency_name: str, currency_description: str,
                                               currency_id: str) -> json:
        data = {
            "currencyAccountName": currency_name,
            "currencyAccountDescription": currency_description
        }
        headers = {'auth_key': auth_key['access_token']}
        res = requests.patch(self.base_url + 'payment-systems-accounts/currency-accounts//' + str(currency_id),
                             headers=headers, json=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
