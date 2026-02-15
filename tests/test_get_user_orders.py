import requests
import allure
import urls
from data import DataMessages


class TestGetUserOrder:
    """
    Тесты для проверки получения заказов пользователя через API.
    """

    @allure.title('Получаем заказы авторизованного пользователя - позитивная проверка')
    def test_get_authorised_user_orders_positive_check(self, client):
        """
        Проверяет получение списка заказов авторизованного пользователя.

        :param client: фикстура, возвращающая (user_data, access_token)
        """
        _, access_token = client

        response = requests.get(
            urls.BASE_URL + urls.ORDERS_ENDPOINT,
            headers={'Authorization': access_token}
        )

        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        resp_json = response.json()
        assert resp_json.get('success') is True, "Поле 'success' должно быть True"

        orders = resp_json.get('orders', [])
        assert len(orders) == 3, f"Ожидалось 3 заказа, получено {len(orders)}"

        total = resp_json.get('total')
        total_today = resp_json.get('totalToday')
        assert total != 0, "Общее количество заказов не должно быть 0"
        assert total_today != 0, "Количество заказов за сегодня не должно быть 0"

    @allure.title('Получаем заказы неавторизованного пользователя (гостя) - негативная проверка')
    def test_get_unauthorised_user_orders_negative_check(self):
        """
        Проверяет, что получение заказов без авторизации возвращает ошибку 401.
        """
        response = requests.get(urls.BASE_URL + urls.ORDERS_ENDPOINT)

        assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"

        resp_json = response.json()
        assert resp_json.get('success') is False, "Поле 'success' должно быть False при ошибке"
        assert resp_json.get('message') == DataMessages.UNAUTHORISED_USER, \
            f"Сообщение об ошибке должно быть '{DataMessages.UNAUTHORISED_USER}'"