import requests
import allure
import urls
from api_helper import create_list_ingredients
from data import DataMessages


class TestCreateOrder:
    """
    Тесты для проверки создания заказов через API.
    Проверяется создание заказов авторизованными и неавторизованными пользователями,
    а также негативные сценарии с некорректными данными.
    """

    @allure.title('Создаем заказ авторизованным пользователем - позитивная проверка')
    def test_create_order_authorised_user_positive_check(self, client):
        """
        Проверка создания заказа авторизованным пользователем.

        :param client: фикстура, возвращающая (user_data, access_token)
        """
        _, access_token = client

        order = {'ingredients': create_list_ingredients()}
        response = requests.post(
            urls.BASE_URL + urls.ORDERS_ENDPOINT,
            headers={'Authorization': access_token},
            json=order  # Используем json, а не data
        )

        assert response.status_code == 200

        resp_json = response.json()
        assert resp_json.get('name'), "В ответе отсутствует название заказа"
        assert resp_json.get('order', {}).get('number'), "В заказе отсутствует номер"
        assert resp_json.get('success') is True

    @allure.title('Создаем заказ неавторизованным пользователем (гостем) - позитивная проверка')
    def test_create_order_unauthorised_user_positive_check(self):
        """
        Проверка создания заказа неавторизованным (гостевым) пользователем.
        """
        order = {'ingredients': create_list_ingredients()}
        response = requests.post(
            urls.BASE_URL + urls.ORDERS_ENDPOINT,
            json=order
        )

        assert response.status_code == 200

        resp_json = response.json()
        assert resp_json.get('name'), "В ответе отсутствует название заказа"
        assert resp_json.get('order', {}).get('number'), "В заказе отсутствует номер"
        assert resp_json.get('success') is True

    @allure.title('Создаем заказ без ингредиентов - негативная проверка')
    def test_create_order_empty_ingredients_list_negative_check(self):
        """
        Проверка создания заказа с пустым списком ингредиентов.
        Ожидается ошибка 400 и соответствующее сообщение об ошибке.
        """
        order = {'ingredients': []}
        response = requests.post(
            urls.BASE_URL + urls.ORDERS_ENDPOINT,
            json=order
        )

        assert response.status_code == 400

        resp_json = response.json()
        assert resp_json.get('success') is False
        assert resp_json.get('message') == DataMessages.CREATE_ORDER_EMPTY_INGREDIENTS

    @allure.title('Создаем заказ с неверным хешем ингредиентов - негативная проверка')
    def test_create_order_false_hash_ingredients_negative_check(self):
        """
        Проверка создания заказа с неправильным хешем ингредиентов.
        """
        order = {'ingredients': ['abracadabra100', 'superkalifragiristikexpialidoshes']}
        response = requests.post(
            urls.BASE_URL + urls.ORDERS_ENDPOINT,
            json=order
        )

        assert response.status_code == 500