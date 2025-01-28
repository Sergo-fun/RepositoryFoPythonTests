import json
import httpx
import pytest
from jsonschema import validate
import allure
from core.contracts import REGISTERED_USER_SCHEME, UNSUCCESS_REGISTER_SCHEME, LOGIN_USER_SCHEME

# Загрузка данных пользователей
json_file = open('D:/Python/core/new_users_data.json')
json_file_invalid = open('D:/Python/core/invalid_users_data.json')

users_data = json.load(json_file)
users_data_invalid = json.load(json_file_invalid)
print(users_data)

BASE_URL = "https://reqres.in/"
REGISTER_USER = "api/register"
LOGIN_USER = "api/login"


@pytest.mark.parametrize('users_data', users_data)
@allure.suite("Регистрация пользователя")
@allure.title("Успешная регистрация пользователя")
@allure.severity(allure.severity_level.CRITICAL)
def test_successful_register(users_data):
    with allure.step("Отправка запроса на регистрацию"):
        response = httpx.post(BASE_URL + REGISTER_USER, json=users_data)

    assert response.status_code == 200
    with allure.step("Проверка соответствия схемы ответа"):
        validate(response.json(), REGISTERED_USER_SCHEME)


@pytest.mark.parametrize('users_data_invalid', users_data_invalid)
@allure.suite("Регистрация пользователя")
@allure.title("Неуспешная регистрация пользователя")
@allure.severity(allure.severity_level.NORMAL)
def test_unsuccessful_register(users_data_invalid):
    with allure.step("Отправка запроса с некорректными данными для регистрации"):
        response = httpx.post(BASE_URL + REGISTER_USER, json=users_data_invalid)

    assert response.status_code == 400
    with allure.step("Проверка json ответа на ошибку"):
        validate(response.json(), UNSUCCESS_REGISTER_SCHEME)


@pytest.mark.parametrize('users_data', users_data)
@allure.suite("Вход пользователя")
@allure.title("Успешный вход пользователя")
@allure.severity(allure.severity_level.CRITICAL)
def test_successful_login(users_data):
    with allure.step("Отправка запроса на вход"):
        response = httpx.post(BASE_URL + LOGIN_USER, json=users_data)

    assert response.status_code == 200
    with allure.step("Проверка json ответа на успешный вход"):
        validate(response.json(), LOGIN_USER_SCHEME)
