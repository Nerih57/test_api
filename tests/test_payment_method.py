import pytest

from api.api_get_token import BillingApiToken
from api.api_payment_method import BillingApiPaymentMethod
from settings import user_data_valid, number_page, limit_data, sort_direction_for, active, wrong_id

get_token = BillingApiToken()
payment_method = BillingApiPaymentMethod()


def test_all_payment_methods(page=number_page, limit=limit_data, sort_direction=sort_direction_for):
    """Метод находит и возвращает список платёжных систем
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_payment_settings/getPaymentMethods.md"""
    sort_column = ['paymentMethodName']
    _, auth_key = get_token.get_api_key(user_data_valid)
    status, result = payment_method.get_all_payments_methods(auth_key, page, limit[0], sort_column[0], sort_direction[0])
    assert status == 200
    assert len(result['items']) > 0
    status, result = payment_method.get_all_payments_methods(auth_key, page, limit[1], sort_column[0], sort_direction[1])
    assert status == 200
    assert len(result['items']) > 0


def test_info_payment_method(page=number_page, limit=limit_data, sort_direction=sort_direction_for,
                             incorrect_id=wrong_id):
    """Метод возвращает карточку одной платежной системы по её идентификатору
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_payment_settings/updatePaymentMethod.md"""
    sort_column = ['paymentMethodName']
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = payment_method.get_all_payments_methods(auth_key, page, limit[0], sort_column[0], sort_direction[0])
    id_pm = result['items'][0]['id']
    status, result = payment_method.get_info_payment_method(auth_key, id_pm)
    assert status == 200
    assert len(result['id']) > 0
    status, result = payment_method.get_info_payment_method(auth_key, incorrect_id)
    assert status == 404
    assert result['errorCode'] == 'PAYMENT_METHOD_NOT_FOUND'


def test_update_payment_method(page=number_page, limit=limit_data, sort_direction=sort_direction_for,
                               incorrect_id=wrong_id):
    """Метод обновляет все поля для одного экземпляра платежной системы.
    Ссылка на описание - https://gitlab.idynsys.org/wlb_project/b2b/analytics/b2b-sa-documentation/-/blob/main/Backend/
    Billing/billing-settings/endpoints_payment_settings/updatePaymentSystem.md#updatepaymentsystem"""
    description = "test"
    sort_column = ['paymentMethodName']
    _, auth_key = get_token.get_api_key(user_data_valid)
    _, result = payment_method.get_all_payments_methods(auth_key, page, limit[0], sort_column[0], sort_direction[0])
    id_pm = result['items'][0]['id']
    status, result = payment_method.patch_update_payment_method(auth_key, description, id_pm)
    assert status == 200
    _, result = payment_method.get_info_payment_method(auth_key, id_pm)
    assert result['paymentMethodDescription'] == description
    status, result = payment_method.patch_update_payment_method(auth_key, description, incorrect_id)
    assert status == 404
    assert result['errorCode'] == 'PAYMENT_METHOD_NOT_FOUND'
