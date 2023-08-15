import pytest
import random

from api.api_get_token import BillingApiToken
from api.api_payment_settings import BillingApiPaymentSettings
from settings import user_data_valid, number_page, limit_data, sort_direction_for, active, wrong_id

get_token = BillingApiToken()
payment_system = BillingApiPaymentSettings()


def test_all_payment_system(page=number_page, limit=limit_data, sort_direction=sort_direction_for):
    """Метод находит и возвращает список платёжных систем
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_payment_settings/searchPaymentSystems.md"""
    sort_column = ['paymentSystemName', 'paymentMethodsCount', 'isActive']
    _, auth_key = get_token.get_api_key(user_data_valid)
    status, result = payment_system.get_all_payments_system(auth_key, page, limit[0], sort_column[0], sort_direction[0])
    assert status == 200
    assert len(result['itemsList']) > 0
    status, result = payment_system.get_all_payments_system(auth_key, page, limit[1], sort_column[1], sort_direction[1])
    assert status == 200
    assert len(result['itemsList']) > 0
    status, result = payment_system.get_all_payments_system(auth_key, page, limit[2], sort_column[2], sort_direction[0])
    assert status == 200
    assert len(result['itemsList']) > 0


def test_info_payment_system(page=number_page, limit=limit_data, sort_direction=sort_direction_for,
                             incorrect_id=wrong_id):
    """Метод возвращает карточку одной платежной системы по её идентификатору
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_payment_settings/getPaymentSystemCard.md"""
    sort_column = ['paymentSystemName', 'paymentMethodsCount', 'isActive']
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = payment_system.get_all_payments_system(auth_key, page, limit[0], sort_column[0], sort_direction[0])
    id_ps = result['itemsList'][0]['id']
    status, result = payment_system.get_info_payment_system(auth_key, id_ps)
    assert status == 200
    assert len(result['id']) > 0
    status, result = payment_system.get_info_payment_system(auth_key, incorrect_id)
    assert status == 404
    assert result['errorCode'] == 'PAYMENT_SYSTEM_NOT_FOUND'


def test_update_payment_system(is_active=active, page=number_page, limit=limit_data, sort_direction=sort_direction_for,
                               incorrect_id=wrong_id):
    """Метод обновляет все поля для одного экземпляра платежной системы.
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_payment_settings/updatePaymentSystem.md#updatepaymentsystem"""
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


def test_all_payment_methods_for_ps(page=number_page, limit=limit_data, sort_direction=sort_direction_for,
                                    incorrect_id=wrong_id):
    """Метод возвращает список платежных методов
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_payment_settings/getPaymentMethods.md#getpaymentmethods"""
    sort_column = ['paymentMethodName']
    sort_column_for_ps = ['paymentSystemName', 'paymentMethodsCount', 'isActive']
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = payment_system.get_all_payments_system(auth_key, page, limit[0], sort_column_for_ps[0],
                                                       sort_direction[0])
    id_ps = result['itemsList'][0]['id']
    status, result = payment_system.get_all_payments_methods_for_ps(auth_key, page, limit[0], sort_column[0],
                                                                    sort_direction[0], id_ps)
    assert status == 200
    assert len(result['items']) > 0
    status, result = payment_system.get_all_payments_methods_for_ps(auth_key, page, limit[1], sort_column[0],
                                                                    sort_direction[1], id_ps)
    assert status == 200
    assert len(result['items']) > 0
    status, result = payment_system.get_all_payments_methods_for_ps(auth_key, page, limit[2], sort_column[0],
                                                                    sort_direction[0], id_ps)
    assert status == 200
    assert len(result['items']) > 0
    status, result = payment_system.get_all_payments_methods_for_ps(auth_key, page, limit[0], sort_column[0],
                                                                    sort_direction[1], incorrect_id)
    assert status == 200
    assert len(result['items']) == 0


def test_info_payment_method(page=number_page, limit=limit_data, sort_direction=sort_direction_for,
                             incorrect_id=wrong_id):
    """Метод возвращает карточку платежного метода
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_payment_settings/getPaymentMethodCard.md#getpaymentmethodcard"""
    sort_column = ['paymentMethodName']
    sort_column_for_ps = ['paymentSystemName', 'paymentMethodsCount', 'isActive']
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = payment_system.get_all_payments_system(auth_key, page, limit[0], sort_column_for_ps[0],
                                                       sort_direction[0])
    id_ps = result['itemsList'][0]['id']
    _, result = payment_system.get_all_payments_methods_for_ps(auth_key, page, limit[0], sort_column[0],
                                                               sort_direction[0], id_ps)
    id_pm = result['items'][0]['id']
    status, result = payment_system.get_info_payment_method(auth_key, id_pm)
    assert status == 200
    assert result['id'] == id_pm
    status, result = payment_system.get_info_payment_method(auth_key, incorrect_id)
    assert status == 404
    assert result['errorCode'] == 'ENTITY_NOT_FOUND'


def test_update_payment_method(is_active=active, page=number_page, limit=limit_data, sort_direction=sort_direction_for,
                               incorrect_id=wrong_id):
    """Метод обновляет все поля для одного экземпляра валюты.
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_currencies/updateCurrency.md"""
    sort_column = ['paymentMethodName']
    sort_column_for_ps = ['paymentSystemName', 'paymentMethodsCount', 'isActive']
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = payment_system.get_all_payments_system(auth_key, page, limit[0], sort_column_for_ps[0],
                                                       sort_direction[0])
    id_ps = result['itemsList'][0]['id']
    _, result = payment_system.get_all_payments_methods_for_ps(auth_key, page, limit[0], sort_column[0],
                                                               sort_direction[0], id_ps)
    id_pm = result['items'][0]['id']
    status, result = payment_system.patch_update_payment_method(auth_key, is_active[0], id_pm)
    assert status == 200
    _, result = payment_system.get_info_payment_method(auth_key, id_pm)
    assert result['isActive'] == is_active[0]
    status, result = payment_system.patch_update_payment_method(auth_key, is_active[1], id_pm)
    assert status == 200
    _, result = payment_system.get_info_payment_method(auth_key, id_pm)
    assert result['isActive'] == is_active[1]
    status, result = payment_system.patch_update_payment_method(auth_key, is_active[0], incorrect_id)
    assert status == 404
    assert result['errorCode'] == 'ENTITY_NOT_FOUND'


def test_all_organization_for_ps(page=number_page, limit=limit_data, sort_direction=sort_direction_for,
                                 incorrect_id=wrong_id):
    """Метод возвращает список организаций для одной платежной системы с признаком активации
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_payment_settings/getPaymentSystemOrganizations.md"""
    sort_column = ['organizationTitle', 'organizationType', 'isPaymentSystemActiveForOrganization']
    sort_column_for_ps = ['paymentSystemName', 'paymentMethodsCount', 'isActive']
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = payment_system.get_all_payments_system(auth_key, page, limit[0], sort_column_for_ps[0],
                                                       sort_direction[0])
    id_ps = result['itemsList'][0]['id']
    status, result = payment_system.get_all_organization_for_ps(auth_key, page, limit[0], sort_column[0],
                                                                sort_direction[0], id_ps)
    assert status == 200
    assert len(result['itemsList']) >= 0
    status, result = payment_system.get_all_organization_for_ps(auth_key, page, limit[1], sort_column[1],
                                                                sort_direction[1], id_ps)
    assert status == 200
    assert len(result['itemsList']) >= 0
    status, result = payment_system.get_all_organization_for_ps(auth_key, page, limit[2], sort_column[2],
                                                                sort_direction[0], id_ps)
    assert status == 200
    assert len(result['itemsList']) >= 0
    status, result = payment_system.get_all_organization_for_ps(auth_key, page, limit[0], sort_column[0],
                                                                sort_direction[1], incorrect_id)
    assert status == 200
    assert len(result['itemsList']) >= 0


def test_update_active_organization_for_ps(page=number_page, limit=limit_data, sort_direction=sort_direction_for,
                                           incorrect_id=wrong_id):
    """Метод устанавливает статус связки между указанный платежной системой и организацией на полученный в теле запроса
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_payment_settings/updateOrganizationActivation.md#updateorganizationactivation"""
    sort_column = ['organizationTitle', 'organizationType', 'isPaymentSystemActiveForOrganization']
    sort_column_for_ps = ['paymentSystemName', 'paymentMethodsCount', 'isActive']
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = payment_system.get_all_payments_system(auth_key, page, limit[0], sort_column_for_ps[0],
                                                       sort_direction[0])
    id_ps = result['itemsList'][0]['id']
    status, result = payment_system.get_all_organization_for_ps(auth_key, page, limit[0], sort_column[0],
                                                                sort_direction[0], id_ps)
    id_organization = result['itemsList'][0]['organizationId']
    status, result = payment_system.put_update_active_organization(auth_key, active[0], id_ps, id_organization)
    assert status == 200
    _, result = payment_system.get_all_organization_for_ps(auth_key, page, limit[0], sort_column[0],
                                                           sort_direction[0], id_ps)
    assert result['itemsList'][0]['isPaymentSystemActiveForOrganization'] == active[0]
    status, result = payment_system.put_update_active_organization(auth_key, active[1], id_ps, id_organization)
    assert status == 200
    _, result = payment_system.get_all_organization_for_ps(auth_key, page, limit[0], sort_column[0],
                                                           sort_direction[0], id_ps)
    assert result['itemsList'][0]['isPaymentSystemActiveForOrganization'] == active[1]
    status, result = payment_system.put_update_active_organization(auth_key, active[0], incorrect_id, id_organization)
    assert status == 404
    assert result['errorCode'] == 'PAYMENT_SYSTEM_NOT_FOUND'
    status, result = payment_system.put_update_active_organization(auth_key, active[0], id_ps, incorrect_id)
    assert status == 404
    assert result['errorCode'] == 'ORGANIZATION_NOT_FOUND'


def test_get_active_organization_for_ps(page=number_page, limit=limit_data, sort_direction=sort_direction_for,
                                        incorrect_id=wrong_id):
    """Метод возвращает список активированных организаций для одной платежной системы
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_payment_settings/getActiveOrganizationsForPaymentSystem.md
    #getactiveorganizationsforpaymentsystem"""
    sort_column_for_ps = ['paymentSystemName', 'paymentMethodsCount', 'isActive']
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = payment_system.get_all_payments_system(auth_key, page, limit[0], sort_column_for_ps[0],
                                                       sort_direction[0])
    id_ps = result['itemsList'][0]['id']
    status, result = payment_system.get_active_organization_for_ps(auth_key, id_ps)
    assert status == 200
    assert len(result['itemsList']) >= 0
    status, result = payment_system.get_active_organization_for_ps(auth_key, incorrect_id)
    assert status == 200
    assert len(result['itemsList']) == 0


def test_get_payment_systems_for_organization(page=number_page, limit=limit_data, sort_direction=sort_direction_for,
                                              incorrect_id=wrong_id):
    """Метод устанавливает статус связки между указанный платежной системой и организацией на полученный в теле запроса
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_payment_settings/updateOrganizationActivation.md#updateorganizationactivation"""
    sort_column_for_organization = ['organizationTitle', 'organizationType', 'isPaymentSystemActiveForOrganization']
    sort_column_for_ps = ['paymentSystemName', 'paymentMethodsCount', 'isPaymentSystemActiveForOrganization']
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = payment_system.get_all_payments_system(auth_key, page, limit[0], sort_column_for_ps[0],
                                                       sort_direction[0])
    id_ps = result['itemsList'][0]['id']
    status, result = payment_system.get_all_organization_for_ps(auth_key, page, limit[0],
                                                                sort_column_for_organization[0], sort_direction[0],
                                                                id_ps)
    id_organization = result['itemsList'][0]['organizationId']
    status, result = payment_system.get_all_ps_for_organization(auth_key, page, limit[0], sort_column_for_ps[0],
                                                                sort_direction[0], id_organization)
    assert status == 200
    assert len(result['itemsList']) > 0 and result['itemsList'][0]['paymentSystemId'] == id_ps
    status, result = payment_system.get_all_ps_for_organization(auth_key, page, limit[0], sort_column_for_ps[0],
                                                                sort_direction[0], incorrect_id)
    assert status == 200
    assert len(result['itemsList']) >= 0


def test_filter_payment_methods_for_ps(page=number_page, limit=limit_data, is_active=active,
                                       sort_direction=sort_direction_for):
    """Метод возвращает список платежных методов
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_payment_settings/getPaymentMethods.md#getpaymentmethods"""
    sort_column_for_ps = ['paymentSystemName', 'paymentMethodsCount', 'isActive']
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = payment_system.get_all_payments_system(auth_key, page, limit[0], sort_column_for_ps[0],
                                                       sort_direction[0])
    id_ps = result['itemsList'][0]['id']
    status, result = payment_system.get_filter_payments_methods_for_ps(auth_key, page, limit[0], is_active[0], id_ps)
    assert status == 200
    assert len(result['items']) >= 0
    status, result = payment_system.get_filter_payments_methods_for_ps(auth_key, page, limit[0], is_active[1], id_ps)
    assert status == 200
    assert len(result['items']) >= 0


def test_filter_organization_for_ps(page=number_page, limit=limit_data, sort_direction=sort_direction_for,
                                    is_active=active):
    """Метод возвращает список организаций для одной платежной системы с признаком активации
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_payment_settings/getPaymentSystemOrganizations.md"""
    organization_type = ['exploitation_team', 'vendor', 'platform']
    sort_column_for_ps = ['paymentSystemName', 'paymentMethodsCount', 'isActive']
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = payment_system.get_all_payments_system(auth_key, page, limit[0], sort_column_for_ps[0],
                                                       sort_direction[0])
    id_ps = result['itemsList'][0]['id']
    status, result = payment_system.get_filter_organization_for_ps(auth_key, page, limit[0], is_active[0],
                                                                   organization_type[0], id_ps)
    assert status == 200
    assert len(result['itemsList']) >= 0
    status, result = payment_system.get_filter_organization_for_ps(auth_key, page, limit[0], is_active[1],
                                                                   organization_type[1], id_ps)
    assert status == 200
    assert len(result['itemsList']) >= 0
    status, result = payment_system.get_filter_organization_for_ps(auth_key, page, limit[0], is_active[0:1],
                                                                   organization_type[2], id_ps)
    assert status == 200
    assert len(result['itemsList']) >= 0
    status, result = payment_system.get_filter_organization_for_ps(auth_key, page, limit[0], is_active[0],
                                                                   organization_type[0:2], id_ps)
    assert status == 200
    assert len(result['itemsList']) >= 0
