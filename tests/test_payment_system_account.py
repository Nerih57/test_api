import pytest
import random

from api.api_get_token import BillingApiToken
from api.api_payment_settings import BillingApiPaymentSettings
from api.api_payment_system_account import BillingApiPaymentSettingsAccounts
from api.api_currencies import BillingApiCurrencies
from settings import user_data_valid, number_page, limit_data, sort_direction_for, active, wrong_id

get_token = BillingApiToken()
payment_system = BillingApiPaymentSettings()
ps_account = BillingApiPaymentSettingsAccounts()
currencies = BillingApiCurrencies()


def test_get_all_payment_system_account(page=number_page, limit=limit_data, sort_direction=sort_direction_for):
    """Возвращает список учетных записей организаций для платежных систем по заданным параметрам поиска и сортировки
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_psa/searchPaymentSystemAccounts.md#searchpaymentsystemaccounts"""
    sort_column = ['paymentSystemAccountName', 'organizationName', 'paymentSystemName', 'currencyAccountCount']
    _, auth_key = get_token.get_api_key(user_data_valid)
    status, result = ps_account.get_all_payments_system_accounts(auth_key, page, limit[0], sort_column[0],
                                                                 sort_direction[0])
    assert status == 200
    assert len(result['itemsList']) > 0
    status, result = ps_account.get_all_payments_system_accounts(auth_key, page, limit[1], sort_column[1],
                                                                 sort_direction[1])
    assert status == 200
    assert len(result['itemsList']) > 0
    status, result = ps_account.get_all_payments_system_accounts(auth_key, page, limit[2], sort_column[2],
                                                                 sort_direction[0])
    assert status == 200
    assert len(result['itemsList']) > 0
    status, result = ps_account.get_all_payments_system_accounts(auth_key, page, limit[0], sort_column[3],
                                                                 sort_direction[1])
    assert status == 200
    assert len(result['itemsList']) > 0


def test_info_payment_system_account(page=number_page, limit=limit_data, sort_direction=sort_direction_for,
                                     incorrect_id=wrong_id):
    """Метод возвращает карточку одного аккаунта платежной системы по идентификатору
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_psa/getPaymentSystemAccountCard.md#getpaymentsystemaccountcard"""
    sort_column = ['paymentSystemAccountName', 'organizationName', 'paymentSystemName', 'currencyAccountCount']
    _, auth_key = get_token.get_api_key(user_data_valid)
    status, result = ps_account.get_all_payments_system_accounts(auth_key, page, limit[0], sort_column[0],
                                                                 sort_direction[0])
    id_psa = result['itemsList'][0]['id']
    status, result = ps_account.get_info_payment_system_account(auth_key, id_psa)
    assert status == 200
    assert len(result['id']) > 0
    status, result = ps_account.get_info_payment_system_account(auth_key, incorrect_id)
    assert status == 404
    assert result['errorCode'] == 'PAYMENT_SYSTEM_ACCOUNT_NOT_FOUND'


@pytest.mark.xfail
def test_post_add_payment_system_account(page=number_page, limit=limit_data, sort_direction=sort_direction_for,
                                         incorrect_id=wrong_id):
    """Метод добавляет одну учётную запись в платежной системе для одной организации
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_psa/addPaymentSystemAccount.md#addpaymentsystemaccount"""
    sort_column_for_ps = ['paymentSystemName', 'paymentMethodsCount', 'isActive']
    description = "test"
    name_psa = 'test_auto_' + str(random.randrange(1000))
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = payment_system.get_all_payments_system(auth_key, page, limit[0], sort_column_for_ps[0],
                                                       sort_direction[0])
    id_ps = result['itemsList'][0]['id']
    status, result = payment_system.get_active_organization_for_ps(auth_key, id_ps)
    id_organization = result['itemsList'][0]['organizationId']
    status, result = ps_account.post_add_ps_account(auth_key, name_psa, description, id_organization, id_ps)
    assert status == 201
    assert len(result['id']) > 0
    id_psa = result['id']
    status, result = ps_account.get_info_payment_system_account(auth_key, id_psa)
    assert status == 200
    assert result['paymentSystemAccountName'] == name_psa and result['paymentSystemAccountDescription'] == description \
           and result['paymentSystemId'] == id_ps
    status, result = ps_account.post_add_ps_account(auth_key, name_psa, description, id_organization, id_ps)
    assert status == 409
    assert result['errorCode'] == 'PAYMENT_SYSTEM_ACCOUNT_NAME_NOT_UNIQUE'
    status, result = ps_account.post_add_ps_account(auth_key, name_psa, description, incorrect_id, id_ps)
    assert status == 200
    assert len(result) == 0
    status, result = ps_account.post_add_ps_account(auth_key, name_psa, description, id_organization, incorrect_id)
    assert status == 499
    assert result['errorCode'] == 'COULD_NOT_SAVE_PAYMENT_SYSTEM_ORGANIZATION_ACCOUNTS'


def test_update_payment_system_account(is_active=active, page=number_page, limit=limit_data,
                                       sort_direction=sort_direction_for, incorrect_id=wrong_id):
    """Метод обновляет поля для одного экземпляра аккаунта платежной системы.
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_psa/updatePaymentSystemAccount.md#updatepaymentsystemaccount"""
    description = "test"
    name_ps = 'test_auto_' + str(random.randrange(1000))
    sort_column = ['paymentSystemName', 'paymentMethodsCount', 'isActive']
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = payment_system.get_all_payments_system(auth_key, page, limit[0], sort_column[0], sort_direction[0])
    id_ps = result['itemsList'][0]['id']
    existing_name = result['itemsList'][1]['paymentSystemName']
    status, result = payment_system.patch_update_payment_system(auth_key, name_ps, description, is_active[0], id_ps)
    assert status == 200
    _, result = payment_system.get_info_payment_system(auth_key, id_ps)
    assert result['paymentSystemName'] == name_ps and result['paymentSystemDescription'] == description \
           and result['isActive'] == is_active[0]
    status, result = payment_system.patch_update_payment_system(auth_key, name_ps, description, is_active[1], id_ps)
    assert status == 200
    _, result = payment_system.get_info_payment_system(auth_key, id_ps)
    assert result['paymentSystemName'] == name_ps and result['paymentSystemDescription'] == description \
           and result['isActive'] == is_active[1]
    status, result = payment_system.patch_update_payment_system(auth_key, name_ps, description, is_active[1],
                                                                incorrect_id)
    assert status == 404
    assert result['errorCode'] == 'PAYMENT_SYSTEM_NOT_FOUND'
    status, result = payment_system.patch_update_payment_system(auth_key, existing_name, description, is_active[1],
                                                                id_ps)
    assert status == 409
    assert result['errorCode'] == 'PAYMENT_SYSTEM_NAME_NOT_UNIQUE'


def test_post_add_currency_account_for_psa(page=number_page, limit=limit_data, sort_direction=sort_direction_for,
                                           incorrect_id=wrong_id):
    """Метод добавляет одну валюту в аккаунт платежной системы
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_psa/addOrganizationCurrencyAccount.md#addorganizationcurrencyaccount"""
    sort_column = ['paymentSystemAccountName', 'organizationName', 'paymentSystemName', 'currencyAccountCount']
    description = "test"
    name_currency_account = 'test_auto_' + str(random.randrange(1000))
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = currencies.get_active_currencies(auth_key)
    iso_currency = result['itemsList'][0]['currencyIsoCode']
    _, result = ps_account.get_all_payments_system_accounts(auth_key, page, limit[0], sort_column[0], sort_direction[0])
    id_psa = result['itemsList'][0]['id']
    status, result = ps_account.post_add_currency_for_ps_account(auth_key, name_currency_account, description,
                                                                 iso_currency, id_psa)
    assert status == 201
    assert len(result['id']) > 0
    status, result = ps_account.post_add_currency_for_ps_account(auth_key, name_currency_account, description,
                                                                 iso_currency, id_psa)
    assert status == 409
    assert result['errorCode'] == 'CURRENCY_ACCOUNT_NAME_NOT_UNIQUE'
    status, result = ps_account.post_add_currency_for_ps_account(auth_key, name_currency_account, description,
                                                                 iso_currency, incorrect_id)
    print(result)
    assert status == 499
    assert result['errorCode'] == 'COULD_NOT_SAVE_CURRENCY_ACCOUNT'


def test_get_all_currency_account_for_psa(page=number_page, limit=limit_data, sort_direction=sort_direction_for,
                                          incorrect_id=wrong_id):
    """Возвращает список валютных счетов в аккаунте платежной системы
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_psa/searchOrganizationCurrencyAccounts.md#searchorganizationcurrencyaccounts"""
    sort_column_for_psa = ['paymentSystemAccountName', 'organizationName', 'paymentSystemName', 'currencyAccountCount']
    sort_column = ['currencyAccountName', 'currencyName', 'currencyIsoCode']
    _, auth_key = get_token.get_api_key(user_data_valid)
    status, result = ps_account.get_all_payments_system_accounts(auth_key, page, limit[0], sort_column_for_psa[0],
                                                                 sort_direction[0])
    id_psa = result['itemsList'][0]['id']
    status, result = ps_account.get_all_currency_accounts_for_psa(auth_key, page, limit[0], sort_column[0],
                                                                  sort_direction[0], id_psa)
    assert status == 200
    assert len(result['itemsList']) > 0
    status, result = ps_account.get_all_currency_accounts_for_psa(auth_key, page, limit[1], sort_column[1],
                                                                  sort_direction[1], id_psa)
    assert status == 200
    assert len(result['itemsList']) > 0
    status, result = ps_account.get_all_currency_accounts_for_psa(auth_key, page, limit[2], sort_column[2],
                                                                  sort_direction[0], id_psa)
    assert status == 200
    assert len(result['itemsList']) > 0
    status, result = ps_account.get_all_currency_accounts_for_psa(auth_key, page, limit[2], sort_column[2],
                                                                  sort_direction[0], incorrect_id)
    assert status == 200
    assert len(result['itemsList']) == 0


def test_info_currency_account_for_psa(page=number_page, limit=limit_data, sort_direction=sort_direction_for,
                                       incorrect_id=wrong_id):
    """Метод возвращает карточку одного аккаунта платежной системы по идентификатору
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_psa/getPaymentSystemAccountCard.md#getpaymentsystemaccountcard"""
    sort_column_for_psa = ['paymentSystemAccountName', 'organizationName', 'paymentSystemName', 'currencyAccountCount']
    sort_column = ['currencyAccountName', 'currencyName', 'currencyIsoCode']
    _, auth_key = get_token.get_api_key(user_data_valid)
    status, result = ps_account.get_all_payments_system_accounts(auth_key, page, limit[0], sort_column_for_psa[0],
                                                                 sort_direction[0])
    id_psa = result['itemsList'][0]['id']
    _, result = ps_account.get_all_currency_accounts_for_psa(auth_key, page, limit[0], sort_column[0],
                                                             sort_direction[0], id_psa)
    id_currency = result['itemsList'][0]['id']
    status, result = ps_account.get_info_currency_account_for_psa(auth_key, id_currency)
    assert status == 200
    assert len(result) > 0
    status, result = ps_account.get_info_currency_account_for_psa(auth_key, incorrect_id)
    assert status == 404
    assert result['errorCode'] == 'CURRENCY_ACCOUNT_NOT_FOUND'


def test_update_currency_account_for_psa(page=number_page, limit=limit_data, sort_direction=sort_direction_for,
                                         incorrect_id=wrong_id):
    """Метод обновляет один валютный счёт в аккаунте платежной системы
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_psa/updateOrganizationCurrencyAccount.md#updateorganizationcurrencyaccount"""
    description = "test"
    name_currency = 'test_auto_' + str(random.randrange(1000))
    sort_column_for_psa = ['paymentSystemAccountName', 'organizationName', 'paymentSystemName', 'currencyAccountCount']
    sort_column = ['currencyAccountName', 'currencyName', 'currencyIsoCode']
    _, auth_key = get_token.get_api_key(user_data_valid)
    status, result = ps_account.get_all_payments_system_accounts(auth_key, page, limit[0], sort_column_for_psa[0],
                                                                 sort_direction[0])
    id_psa = result['itemsList'][0]['id']
    _, result = ps_account.get_all_currency_accounts_for_psa(auth_key, page, limit[0], sort_column[0],
                                                             sort_direction[0], id_psa)
    id_currency = result['itemsList'][0]['id']
    existing_name = result['itemsList'][1]['currencyAccountName']
    status, result = ps_account.patch_update_currency_account_fore_psa(auth_key, name_currency, description,
                                                                       id_currency)
    assert status == 200
    _, result = ps_account.get_info_currency_account_for_psa(auth_key, id_currency)
    assert result['currencyAccountName'] == name_currency and result['currencyAccountDescription'] == description
    status, result = ps_account.patch_update_currency_account_fore_psa(auth_key, name_currency, description,
                                                                       incorrect_id)
    assert status == 200
    assert len(result) == 0
    status, result = ps_account.patch_update_currency_account_fore_psa(auth_key, existing_name, description,
                                                                       id_currency)
    assert status == 409
    assert result['errorCode'] == 'CURRENCY_ACCOUNT_NAME_NOT_UNIQUE'
