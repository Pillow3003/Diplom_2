import requests
import urls
import allure


@allure.step('Регистрируем нового пользователя')
def user_registration(user_data):
    """
    Выполняет POST-запрос на регистрацию нового пользователя.

    :param user_data: dict с данными пользователя (например, name, email, password)
    :return: объект Response от requests
    """
    response = requests.post(
        urls.BASE_URL + urls.REGISTRATION_USER_ENDPOINT,
        json=user_data  
    )
    return response


@allure.step('Формируем перечень ингредиентов для оформления заказа')
def create_list_ingredients():
    """
    Получает список ингредиентов и формирует из них список из 3 выбранных id.

    :return: список из 3 id ингредиентов (list[str])
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


@allure.step('Оформляем заказ авторизованного пользователя')
def create_new_order(access_token):
    """
    Создаёт новый заказ с выбранными ингредиентами.

    :param access_token: str - токен авторизации пользователя
    :return: объект Response от requests
    """
    order = {
        'ingredients': create_list_ingredients()
    }
    headers = {'Authorization': access_token}

    response = requests.post(
        urls.BASE_URL + urls.ORDERS_ENDPOINT,
        headers=headers,
        json=order 
    )
    return response