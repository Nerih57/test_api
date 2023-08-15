import json
import requests

from settings_private import base_url


class BillingApiCurrencies:
    def __init__(self):
        self.base_url = base_url

    def get_all_currencies(self, auth_key: json, page: str, limit: str, sort_column: str, sort_direction: str) -> json:
        headers = {'auth_key': auth_key['access_token']}
        params = {'page': page, 'limit': limit, 'sort_column': sort_column, 'sort_direction': sort_direction}
        res = requests.get(self.base_url + 'currencies', headers=headers, params=params)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_absent_currencies_list(self, auth_key: json):
        headers = {'auth_key': auth_key['access_token']}
        res = requests.get(self.base_url + 'currencies/absent-list', headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_info_currency(self, auth_key: json, currency_id: str) -> json:
        headers = {'auth_key': auth_key['access_token']}
        res = requests.get(self.base_url + 'currencies/' + str(currency_id), headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_add_currency(self, auth_key: json, currency_iso_code: str, currency_description: str, active: bool) -> \
            json:
        data = {
                "currencyIsoCode": currency_iso_code,
                "currencyDescription": currency_description,
                "isActive": active
            }
        headers = {'auth_key': auth_key['access_token']}
        res = requests.post(self.base_url + 'currencies', headers=headers, json=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def patch_update_currency(self, auth_key: json, currency_description: str, active: bool, currency_id: str) -> json:
        data = {
                "currencyDescription": currency_description,
                "isActive": active
            }
        headers = {'auth_key': auth_key['access_token']}
        res = requests.patch(self.base_url + 'currencies/' + str(currency_id), headers=headers, json=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_active_currencies(self, auth_key: json) -> json:
        headers = {'auth_key': auth_key['access_token']}
        res = requests.get(self.base_url + 'currencies/active-list', headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_add_exchange_rate(self, auth_key: json, valid_from: str, is_valid_from_now: bool, currency_iso_code: str,
                               exchange_rate: float) -> json:
        data = {
            "validFrom": valid_from,
            "isValidFromNow": is_valid_from_now,
            "currencyIsoCode": currency_iso_code,
            "exchangeRate": exchange_rate
        }
        headers = {'auth_key': auth_key['access_token']}
        res = requests.post(self.base_url + 'currency-exchange-rates', headers=headers, json=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_all_exchange_rates(self, auth_key: json, page: str, limit: str, sort_column: str, sort_direction: str,
                               currency_iso_code: str) -> json:
        headers = {'auth_key': auth_key['access_token']}
        params = {'page': page, 'limit': limit, 'sort_column': sort_column, 'sort_direction': sort_direction,
                  'iso_code': currency_iso_code}
        res = requests.get(self.base_url + 'currency-exchange-rates', headers=headers, params=params)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_data_source_exchange_rates(self, auth_key: json, currency_iso_code: str) -> json:
        headers = {'auth_key': auth_key['access_token']}
        params = {'iso_code': currency_iso_code}
        res = requests.get(self.base_url + 'currency-exchange-rates/data-sources', headers=headers, params=params)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
