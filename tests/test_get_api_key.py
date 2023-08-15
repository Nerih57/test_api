from api.api_get_token import BillingApiToken
from settings_private import user_data_valid

billing_api = BillingApiToken()


def test_get_api_key_for_valid_user(data=user_data_valid):
    """Метод получает валидный токен в формате JSON"""
    status, result = billing_api.get_api_key(data)
    assert status == 200
    assert 'access_token' in result
    return result['access_token']
