import requests
import urls
import allure


@allure.step('Регистрируем нового пользователя')
def user_registration(user_data):
    """
    Выполняет POST-запрос на регистрацию нового пользователя.

    :param user_data: dict с данными пользователя (например, name, email, password)
    :return: объект Response от requests с результатом регистрации
    """
    response = requests.post(
        urls.BASE_URL + urls.REGISTRATION_USER_ENDPOINT,
        json=user_data  
    )
    return response


@allure.step('Авторизация пользователя и получение токена')
def login_user(user_data):
    """
    Выполняет POST-запрос для авторизации пользователя и получения accessToken.

    :param user_data: dict с данными для входа (например, email, password)
    :return: строка accessToken для последующих запросов
    """
    response = requests.post(
        urls.BASE_URL + urls.LOGIN_USER_ENDPOINT,
        json=user_data  
    )
    return response.json()["accessToken"]


@allure.step('Изменяем данные пользователя')
def change_user(access_token: str | None, user_data: dict):
    """
    Отправляет PATCH-запрос для изменения данных пользователя.

    :param access_token: str | None - токен авторизации (если есть)
    :param user_data: dict с обновленными данными пользователя
    :return: объект Response от requests с результатом изменения
    """
    return requests.patch(
        urls.BASE_URL + urls.USER_DATA_ENDPOINT,
        headers={'Authorization': access_token} if access_token else {},
        json=user_data  
    )


@allure.step('Удаляем зарегистрированного пользователя')
def delete_user(access_token):
    """
    Выполняет удаление пользователя по access_token.

    :param access_token: str - токен авторизации пользователя
    :return: объект Response от requests
    """
    headers = {'Authorization': access_token}
    response = requests.delete(urls.BASE_URL + urls.USER_DATA_ENDPOINT, headers=headers)
    response.raise_for_status() 
    return response


@allure.step('Формируем перечень ингредиентов для оформления заказа')
def create_list_ingredients():
    """
    Получает список ингредиентов из API и формирует список из 3 выбранных ID.

    :return: список из 3 строк с id ингредиентов (list[str])
    :raises ValueError: если ингредиентов в ответе меньше 11
    """
    response = requests.get(urls.BASE_URL + urls.INGREDIENTS_ENDPOINT)
    response.raise_for_status()  

    data = response.json().get('data', [])
    if len(data) < 11:
        raise ValueError("Недостаточно ингредиентов в ответе API")

    ingredient1 = data[0]['_id']
    ingredient2 = data[7]['_id']
    ingredient3 = data[10]['_id']

    return [ingredient1, ingredient2, ingredient3]


@allure.step('Оформляем заказ авторизованного пользователя')
def create_new_order(access_token: str | None, ingredients: list):
    """
    Создаёт новый заказ с выбранными ингредиентами.

    :param access_token: str | None - токен авторизации пользователя
    :param ingredients: list - список ID ингредиентов для заказа
    :return: объект Response от requests с результатом создания заказа
    """
    order = {'ingredients': ingredients}
    headers = {'Authorization': access_token} if access_token else {}

    response = requests.post(
        urls.BASE_URL + urls.ORDERS_ENDPOINT,
        headers=headers,
        json=order 
    )
    return response


@allure.step('Получаем список заказов пользователя')
def get_orders(access_token: str | None):
    """
    Выполняет GET-запрос для получения заказов пользователя.

    :param access_token: str | None - токен авторизации пользователя
    :return: объект Response от requests с данными заказов
    """
    return requests.get(
        urls.BASE_URL + urls.ORDERS_ENDPOINT,
        headers={'Authorization': access_token} if access_token else {}
    )
