import pytest

from api.api_get_token import BillingApiToken
from api.api_payment_method_for_application import BillingApiPMForApplication
from settings import user_data_valid, number_page, limit_data, sort_direction_for, active, wrong_id

get_token = BillingApiToken()
pm_for_applications = BillingApiPMForApplication()


def test_all_pm_for_application(page=number_page, limit=limit_data, sort_direction=sort_direction_for):
    """Метод возвращает список платежных методов для одного приложения с признаком активации и количеством роутов
    (пока не реализовано)
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_application_payment_methods/getPaymentMethodToApplicationLinks.md"""
    sort_column = ['paymentMethod', 'isActive']
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = pm_for_applications.get_applications(auth_key)
    id_application = result['data'][0]['id']
    status, result = pm_for_applications.get_all_pm_for_application(auth_key, id_application, page, limit[0],
                                                                    sort_column[0], sort_direction[0])
    assert status == 200
    assert len(result['items']) >= 0
    status, result = pm_for_applications.get_all_pm_for_application(auth_key, id_application, page, limit[1],
                                                                    sort_column[1], sort_direction[1])
    assert status == 200
    assert len(result['items']) >= 0
    status, result = pm_for_applications.get_all_pm_for_application(auth_key, wrong_id, page, limit[1],
                                                                    sort_column[1], sort_direction[1])
    assert status == 200
    assert len(result['items']) == 0


def test_pm_for_application_for_add(page=number_page, limit=limit_data, sort_direction=sort_direction_for):
    """Метод возвращает список платежных методов доступных к добавлению для приложения.
    Доступны для добавления платежные методы из активных платежных систем организации владельца приложения
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_application_payment_methods/getAvailableToAddPaymentMethods.md"""
    sort_column = ['paymentMethodName']
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = pm_for_applications.get_applications(auth_key)
    id_application = result['data'][0]['id']
    status, result = pm_for_applications.get_pm_for_application_for_add(auth_key, id_application, page, limit[0],
                                                                        sort_column[0], sort_direction[0])
    assert status == 200
    assert len(result['items']) >= 0
    status, result = pm_for_applications.get_pm_for_application_for_add(auth_key, wrong_id, page, limit[1],
                                                                        sort_column[0], sort_direction[1])
    assert status == 200
    assert len(result['items']) == 0


def test_pm_for_application(page=number_page, limit=limit_data, sort_direction=sort_direction_for):
    """Метод возвращает значение атрибутов связки между платежным методом и приложением.
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_application_payment_methods/getPaymentMethodToApplicationLink.md"""
    sort_column = ['paymentMethod', 'isActive']
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = pm_for_applications.get_applications(auth_key)
    id_application = result['data'][0]['id']
    _, result = pm_for_applications.get_all_pm_for_application(auth_key, id_application, page, limit[0],
                                                               sort_column[0], sort_direction[0])
    id_application_payment_method = result['items'][0]['id']
    status, result = pm_for_applications.get_pm_for_application(auth_key, id_application_payment_method)
    assert status == 200
    assert result['id'] == id_application_payment_method
    status, result = pm_for_applications.get_pm_for_application(auth_key, wrong_id)
    assert status == 404
    assert result['errorCode'] == 'APPLICATION_PAYMENT_METHOD_NOT_FOUND'


def test_add_pm_for_application(page=number_page, limit=limit_data, sort_direction=sort_direction_for):
    """Метод создает активную связку между платежным методом и приложением.
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_application_payment_methods/addPaymentMethodToApplicationLink.md"""
    sort_column = ['paymentMethodName']
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = pm_for_applications.get_applications(auth_key)
    id_application = result['data'][0]['id']
    _, result = pm_for_applications.get_pm_for_application_for_add(auth_key, id_application, page, limit[0],
                                                                   sort_column[0], sort_direction[0])
    id_payment_method = result['items'][0]['id']
    status, result = pm_for_applications.post_add_pm_for_application(auth_key, id_payment_method, id_application)
    assert status == 201
    assert 'id' in result
    status, result = pm_for_applications.post_add_pm_for_application(auth_key, wrong_id, id_application)
    assert status == 404
    assert result['errorCode'] == 'PAYMENT_METHOD_NOT_FOUND'
    status, result = pm_for_applications.post_add_pm_for_application(auth_key, id_payment_method, wrong_id)
    assert status == 404
    assert result['errorCode'] == 'APPLICATION_NOT_FOUND'


def test_update_pm_for_application(page=number_page, limit=limit_data, sort_direction=sort_direction_for,
                                   is_active=active):
    """Метод меняет значение атрибутов связки между платежным методом и приложением.
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_application_payment_methods/updatePaymentMethodToApplicationLink.md"""
    sort_column = ['paymentMethod', 'isActive']
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = pm_for_applications.get_applications(auth_key)
    id_application = result['data'][0]['id']
    _, result = pm_for_applications.get_all_pm_for_application(auth_key, id_application, page, limit[0],
                                                               sort_column[0], sort_direction[0])
    id_application_payment_method = result['items'][0]['id']
    status, result = pm_for_applications.put_update_pm_for_applications(auth_key, id_application_payment_method,
                                                                        is_active[0])
    assert status == 200
    _, result = pm_for_applications.get_pm_for_application(auth_key, id_application_payment_method)
    assert result['isActive'] == is_active[0]
    status, result = pm_for_applications.put_update_pm_for_applications(auth_key, id_application_payment_method,
                                                                        is_active[1])
    assert status == 200
    _, result = pm_for_applications.get_pm_for_application(auth_key, id_application_payment_method)
    assert result['isActive'] == is_active[1]
    status, result = pm_for_applications.put_update_pm_for_applications(auth_key, wrong_id, is_active[0])
    assert status == 404
    assert result['errorCode'] == 'APPLICATION_PAYMENT_METHOD_NOT_FOUND'


def test_update_activation_pm_for_application(page=number_page, limit=limit_data, sort_direction=sort_direction_for,
                                              is_active=active):
    """Метод меняет статус активности связки между платежным методом и приложением.
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_application_payment_methods/updateActivationPaymentMethodToApplicationLink.md"""
    sort_column = ['paymentMethod', 'isActive']
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = pm_for_applications.get_applications(auth_key)
    id_application = result['data'][0]['id']
    _, result = pm_for_applications.get_all_pm_for_application(auth_key, id_application, page, limit[0],
                                                               sort_column[0], sort_direction[0])
    id_application_payment_method = result['items'][0]['id']
    status, result = pm_for_applications.patch_update_activation_pm_for_applications(auth_key,
                                                                                     id_application_payment_method,
                                                                                     is_active[0])
    assert status == 200
    _, result = pm_for_applications.get_pm_for_application(auth_key, id_application_payment_method)
    assert result['isActive'] == is_active[0]
    status, result = pm_for_applications.patch_update_activation_pm_for_applications(auth_key,
                                                                                     id_application_payment_method,
                                                                                     is_active[1])
    assert status == 200
    _, result = pm_for_applications.get_pm_for_application(auth_key, id_application_payment_method)
    assert result['isActive'] == is_active[1]
    status, result = pm_for_applications.patch_update_activation_pm_for_applications(auth_key, wrong_id, is_active[0])
    assert status == 404
    assert result['errorCode'] == 'APPLICATION_PAYMENT_METHOD_NOT_FOUND'
