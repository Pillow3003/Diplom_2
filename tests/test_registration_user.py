import pytest
import allure
from api_helper import user_registration, delete_user
from data import DataMessages
import copy


class TestUserRegistration:
    """
    Тесты для проверки регистрации пользователей через API.
    """

    @allure.title('Регистрируем уникального пользователя - позитивная проверка')
    def test_create_new_user_positive_check(self, new_user):
        """
        Проверка успешной регистрации нового уникального пользователя.

        :param new_user: фикстура с данными нового пользователя (dict)
        """
        response = user_registration(new_user)
        resp_json = response.json()

        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        assert resp_json.get('success') is True, "Поле 'success' должно быть True"
        assert resp_json.get('user', {}).get('name') == new_user['name'], "Имя пользователя не совпадает"
        assert resp_json.get('user', {}).get('email') == new_user['email'], "Email пользователя не совпадает"
        assert resp_json.get('accessToken'), "accessToken не должен быть пустым"
        assert resp_json.get('refreshToken'), "refreshToken не должен быть пустым"

        delete_user(resp_json['accessToken'])

    @allure.title('Пытаемся зарегистрировать уже существующего пользователя - негативная проверка')
    def test_create_existed_user_negative_check(self, new_user):
        """
        Проверка, что регистрация уже существующего пользователя возвращает ошибку.

        :param new_user: фикстура с данными нового пользователя (dict)
        """
        response_unique = user_registration(new_user)
        resp_unique_json = response_unique.json()

        try:
            response_double = user_registration(new_user)
            resp_double_json = response_double.json()

            assert response_double.status_code == 403, f"Ожидался статус 403, получен {response_double.status_code}"
            assert resp_double_json.get('success') is False, "Поле 'success' должно быть False при ошибке"
            assert resp_double_json.get('message') == DataMessages.NOT_UNIQUE_USER, \
                f"Ожидалось сообщение: '{DataMessages.NOT_UNIQUE_USER}'"
        finally:

            delete_user(resp_unique_json['accessToken'])

    @allure.title('Пытаемся зарегистрировать пользователя с одним из пустых полей - негативная проверка')
    @pytest.mark.parametrize('empty_input', ['name', 'email', 'password'])
    def test_create_user_empty_input_negative_check(self, new_user, empty_input):
        """
        Проверка невозможности регистрации, если одно из полей пустое.

        :param new_user: фикстура с данными нового пользователя (dict)
        :param empty_input: имя поля, которое будет удалено/пустое
        """
        new_user_modified = copy.deepcopy(new_user)
        new_user_modified.pop(empty_input, None)

        response = user_registration(new_user_modified)
        resp_json = response.json()

        assert response.status_code == 403, f"Ожидался статус 403, получен {response.status_code}"
        assert resp_json.get('success') is False, "Поле 'success' должно быть False при ошибке"
        assert resp_json.get('message') == DataMessages.CREATE_EMPTY_USER, \
            f"Ожидалось сообщение: '{DataMessages.CREATE_EMPTY_USER}'"