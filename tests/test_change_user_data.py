import pytest
import requests
import allure
import urls
from helper import RandomUserData
from data import DataMessages


class TestChangeUserData:
    """
    Тесты для проверки изменения данных пользователя через API.
    Включает позитивные проверки с авторизацией и негативные без неё.
    """

    @allure.title('Меняем данные пользователя с авторизацией (имя или почту) - позитивная проверка')
    @pytest.mark.parametrize('new_field', ['name', 'email'])
    def test_change_authorised_user_data_name_or_email_positive_check(self, client, new_field):
        """
        Проверяет успешное изменение поля 'name' или 'email' пользователя
        с корректной авторизацией.

        :param client: фикстура, возвращающая кортеж (user_data, access_token)
        :param new_field: изменяемое поле ('name' или 'email')
        """
        user_data, access_token = client

        # Генерируем новые данные пользователя
        user_data_generator = RandomUserData()
        new_user_data = user_data_generator.user_data_generation()

        # Заменяем указанное поле на новое значением
        user_data[new_field] = new_user_data[new_field]

        # Отправляем PATCH-запрос с авторизацией
        response = requests.patch(
            urls.BASE_URL + urls.USER_DATA_ENDPOINT,
            headers={'Authorization': access_token},
            json=user_data  # рекомендую использовать json вместо data для API с JSON
        )

        assert response.status_code == 200

        response_json = response.json()
        assert response_json.get('success') is True

        user_response = response_json.get('user', {})
        assert user_response.get('name'), "Имя пользователя не должно быть пустым"
        assert user_response.get('email'), "Email пользователя не должен быть пустым"
        assert user_response.get(new_field) == new_user_data[new_field], f"Поле '{new_field}' не обновилось"

    @allure.title('Меняем данные пользователя с авторизацией (пароль) - позитивная проверка')
    def test_change_authorised_user_data_password_positive_check(self, client):
        """
        Проверяет успешное изменение пароля пользователя с авторизацией.

        :param client: фикстура, возвращающая кортеж (user_data, access_token)
        """
        user_data, access_token = client

        user_data_generator = RandomUserData()
        new_user_data = user_data_generator.user_data_generation()

        user_data['password'] = new_user_data['password']

        response = requests.patch(
            urls.BASE_URL + urls.USER_DATA_ENDPOINT,
            headers={'Authorization': access_token},
            json=user_data
        )

        assert response.status_code == 200

        response_json = response.json()
        assert response_json.get('success') is True

        user_response = response_json.get('user', {})
        assert user_response.get('name'), "Имя пользователя не должно быть пустым"
        assert user_response.get('email'), "Email пользователя не должен быть пустым"


    @allure.title('Меняем данные пользователя без авторизации - негативная проверка')
    @pytest.mark.parametrize('new_field', ['name', 'email', 'password'])
    def test_change_unauthorised_user_data_negative_check(self, client, new_field):
        """
        Проверяет невозможность изменения данных пользователя без авторизации.

        :param client: фикстура, возвращающая кортеж (user_data, access_token)
        :param new_field: поле для изменения ('name', 'email' или 'password')
        """
        user_data, _ = client  

        user_data_generator = RandomUserData()
        new_data = user_data_generator.user_data_generation()

        user_data[new_field] = new_data[new_field]

        response = requests.patch(
            urls.BASE_URL + urls.USER_DATA_ENDPOINT,
            json=user_data
        )

        assert response.status_code == 401

        response_json = response.json()
        assert response_json.get('success') is False
        assert response_json.get('message') == DataMessages.UNAUTHORISED_USER