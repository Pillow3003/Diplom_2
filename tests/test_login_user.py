import pytest
import allure
import api_helper
from data import DataMessages
import copy


class TestLoginUser:
    """
    Тесты для проверки логина пользователя через API.
    """

    @allure.title('Авторизуем (логиним) зарегистрированного пользователя - позитивная проверка')
    def test_login_user_positive_check(self, client):
        """
        Проверка успешной авторизации зарегистрированного пользователя.

        :param client: фикстура, которая возвращает кортеж (user_data, access_token)
                       в данном тесте используется только user_data по индексу 0.
        """
        user_data = client[0]

        response = api_helper.login_user(user_data)

        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        resp_json = response.json()

        assert resp_json.get('success') is True, "Поле success должно быть True"
        assert resp_json.get('accessToken'), "accessToken не должен быть пустым"
        assert resp_json.get('refreshToken'), "refreshToken не должен быть пустым"

        user_in_response = resp_json.get('user', {})
        assert user_in_response.get('name') == user_data['name'], "Имя пользователя не совпадает"
        assert user_in_response.get('email') == user_data['email'], "Email пользователя не совпадает"

    @allure.title('Авторизуем пользователя с ошибкой в логине или пароле - негативная проверка')
    @pytest.mark.parametrize('mistake_field', ['email', 'password'])
    def test_login_user_negative_check(self, client, mistake_field):
        """
        Проверка ошибки при неправильном логине или пароле.

        :param client: фикстура с user_data
        :param mistake_field: поле, которое специально искажается ('email' или 'password')
        """
        invalid_user_data = copy.deepcopy(client[0])
        invalid_user_data[mistake_field] = invalid_user_data[mistake_field] + '1'

        response = api_helper.login_user(invalid_user_data)

        assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"

        resp_json = response.json()
        assert resp_json.get('success') is False, "Поле success должно быть False при ошибке"
        assert resp_json.get('message') == DataMessages.INCORRECT_LOGIN_DATA, \
            f"Сообщение об ошибке должно быть '{DataMessages.INCORRECT_LOGIN_DATA}'"
