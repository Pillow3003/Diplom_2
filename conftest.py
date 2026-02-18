import pytest
import api_helper
from helper import RandomUserData


@pytest.fixture(scope="function")
def client():
    user_data = RandomUserData().user_data_generation()
    api_helper.user_registration(user_data)
    access_token = api_helper.login_user(user_data)
    user_data.pop("password")

    yield user_data, access_token

    api_helper.delete_user(access_token)


@pytest.fixture(scope="function")
def non_registration_user():
    user_data = RandomUserData().user_data_generation()
    user_data.pop('password')

    yield user_data

    access_token = api_helper.login_user(user_data).json()["accessToken"]
    api_helper.delete_user(access_token)
