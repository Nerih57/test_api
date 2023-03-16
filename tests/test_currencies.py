import pytest

from api.api_get_token import BillingApiToken
from api.api_currencies import BillingApiCurrencies
from settings import user_data_valid, number_page, limit_data, sort_direction_for, active, wrong_id

get_token = BillingApiToken()
currencies = BillingApiCurrencies()


# def test_get_internal_all_currencies():
#     """Метод возвращает список валют, доступных и активных для использования на платформе
#     Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/b2b-sa-documentation/-/blob/main/Backend/Billing/
#     currencies/endpoints/internal/getCurrencies.md#getcurrencies"""
#     _, auth_key = get_token.get_api_key(user_data_valid)
#     status, result = currencies.get_internal_all_currencies(auth_key)
#     assert status == 200
#     assert result['itemsList']
#
#
# def test_get_internal_specific_currencies():
#     """Метод получает информацию об одной валюте, доступной и активной для использования на платформе
#     Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/b2b-sa-documentation/-/blob/main/Backend/Billing/
#     currencies/endpoints/internal/getCurrencies.md#getcurrencies"""
#     _, auth_key = get_token.get_api_key(user_data_valid)
#     _, result = currencies.get_internal_all_currencies(auth_key)
#     iso_code = result['itemsList'][0]['currencyIsoCode']
#     status, result = currencies.get_internal_specific_currencies(auth_key, iso_code)
#     assert status == 200
#     assert len(result['itemsList']) > 0


def test_all_currencies(page=number_page, limit=limit_data, sort_direction=sort_direction_for):
    """Метод находит и возвращает список валют, доступных для использования на платформе
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/b2b-sa-documentation/-/blob/main/Backend/Billing/
    currencies/endpoints/searchAllowedCurrencies.md"""
    sort_column = ['currencyName', 'currencyIsoCode', 'isActive']
    _, auth_key = get_token.get_api_key(user_data_valid)
    status, result = currencies.get_all_currencies(auth_key, page, limit[0], sort_column[0], sort_direction[0])
    assert status == 200
    assert len(result['itemsList']) > 0
    status, result = currencies.get_all_currencies(auth_key, page, limit[1], sort_column[1], sort_direction[1])
    assert status == 200
    assert len(result['itemsList']) > 0
    status, result = currencies.get_all_currencies(auth_key, page, limit[2], sort_column[2], sort_direction[0])
    assert status == 200
    assert len(result['itemsList']) > 0
    # status, result = currencies.get_all_currencies(auth_key, ' ', ' ', ' ', ' ')
    # assert status == 200
    # assert len(result['itemsList']) > 0


def test_absent_currencies():
    """Метод возвращает список валют, которые могут быть добавлены на платформу
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_currencies/getAbsentCurrenciesList.md#getabsentcurrencieslist"""
    _, auth_key = get_token.get_api_key(user_data_valid)
    status, result = currencies.get_absent_currencies_list(auth_key)
    assert status == 200
    assert len(result['itemsList']) > 0


def test_add_currency(is_active=active):
    """Метод добавляет один экземпляр валюты из ещё не добавленных валют из справочника.
    В интерфейс выводится результат реквеста getAbsentCurrencies, пользователь выбирает валюту
    (currencyName и currencyIsoCode) из выпадающего списка
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_currencies/addCurrency.md"""
    description = "test"
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = currencies.get_absent_currencies_list(auth_key)
    iso_code = result['itemsList'][0]['currencyIsoCode']
    status, result = currencies.post_add_currency(auth_key, iso_code, description, is_active[0])
    assert status == 201
    assert len(result['id']) > 0
    _, result = currencies.get_absent_currencies_list(auth_key)
    iso_code = result['itemsList'][0]['currencyIsoCode']
    status, result = currencies.post_add_currency(auth_key, iso_code, description, is_active[1])
    assert status == 201
    assert len(result['id']) > 0
    status, result = currencies.post_add_currency(auth_key, iso_code, description, is_active[1])
    assert status == 409
    assert result['errorCode'] == 'CURRENCY_NAME_NOT_UNIQUE'
    status, result = currencies.post_add_currency(auth_key, '', description, is_active[1])
    assert status == 499
    assert result['errorCode'] == 'INCORRECT_ISO_CODE'


def test_info_currency(page=number_page, limit=limit_data, sort_direction=sort_direction_for, incorrect_id=wrong_id):
    """Метод возвращает карточку одной валюты по её идентификатору
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_currencies/getCurrencyCard.md"""
    sort_column = ['currencyName', 'currencyIsoCode', 'isActive']
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = currencies.get_all_currencies(auth_key, page, limit[0], sort_column[0], sort_direction[0])
    id_currency = result['itemsList'][0]['id']
    status, result = currencies.get_info_currency(auth_key, id_currency)
    assert status == 200
    assert len(result['id']) > 0
    status, result = currencies.get_info_currency(auth_key, incorrect_id)
    assert status == 404
    assert result['errorCode'] == 'CURRENCY_NOT_FOUND'


@pytest.mark.xfail
def test_update_currency(is_active=active, page=number_page, limit=limit_data, sort_direction=sort_direction_for,
                         incorrect_id=wrong_id):
    """Метод обновляет все поля для одного экземпляра валюты.
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_currencies/updateCurrency.md"""
    description = "test"
    sort_column = ['currencyName', 'currencyIsoCode', 'isActive']
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = currencies.get_all_currencies(auth_key, page, limit[0], sort_column[0], sort_direction[0])
    id_currency = result['itemsList'][0]['id']
    status, result = currencies.patch_update_currency(auth_key, description, is_active[0], id_currency)
    assert status == 200
    _, result = currencies.get_info_currency(auth_key, id_currency)
    assert result['currencyDescription'] == description and result['isActive'] == is_active[0]
    status, result = currencies.patch_update_currency(auth_key, description, is_active[1], id_currency)
    assert status == 200
    _, result = currencies.get_info_currency(auth_key, id_currency)
    assert result['currencyDescription'] == description and result['isActive'] == is_active[1]
    status, result = currencies.patch_update_currency(auth_key, description, is_active[1], incorrect_id)
    assert status == 409
    assert result['errorCode'] == 'CURRENCY_NAME_NOT_UNIQUE'


def test_active_currencies():
    """Метод возвращает список валют, доступных и активных для использования на платформе
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_currencies/getActiveCurrencies.md#getactivecurrencies"""
    _, auth_key = get_token.get_api_key(user_data_valid)
    status, result = currencies.get_active_currencies(auth_key)
    assert status == 200
    assert len(result['itemsList']) > 0
