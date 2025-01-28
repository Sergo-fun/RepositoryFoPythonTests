import datetime
import allure
import httpx
from jsonschema import validate
from core.contracts import CREATE_USER_SCHEME

BASE_URL = "https://reqres.in/"
CREATE_USER = "api/users"


@allure.suite("Create User API")
@allure.title("Создание пользователя с корректными данными")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_user():
    body = {
        "name": "morpheus",
        "job": "leader"
    }
    with allure.step("Отправить POST-запрос для создания пользователя"):
        response = httpx.post(BASE_URL + CREATE_USER, json=body)

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 201

    with allure.step("Проверить схему JSON-ответа и данные"):
        response_json = response.json()
        creation_date = response_json['createdAt'].replace('T', ' ')
        current_date = str(datetime.datetime.utcnow())

        validate(response_json, CREATE_USER_SCHEME)
        assert response_json['name'] == body['name']
        assert response_json['job'] == body['job']
        assert creation_date[0:14] == current_date[0:14]


@allure.suite("Create User API")
@allure.title("Создание пользователя без указания имени")
@allure.severity(allure.severity_level.MINOR)
def test_create_user_without_name():
    body = {
        "job": "leader"
    }
    with allure.step("Отправить POST-запрос для создания пользователя без имени"):
        response = httpx.post(BASE_URL + CREATE_USER, json=body)

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 201

    with allure.step("Проверить схему JSON-ответа и данные"):
        response_json = response.json()
        creation_date = response_json['createdAt'].replace('T', ' ')
        current_date = str(datetime.datetime.utcnow())

        validate(response_json, CREATE_USER_SCHEME)
        assert response_json['job'] == body['job']
        assert creation_date[0:14] == current_date[0:14]


@allure.suite("Create User API")
@allure.title("Создание пользователя без указания профессии")
@allure.severity(allure.severity_level.NORMAL)
def test_create_user_without_job():
    body = {
        "name": "morpheus",
    }
    with allure.step("Отправить POST-запрос для создания пользователя без профессии"):
        response = httpx.post(BASE_URL + CREATE_USER, json=body)

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 201

    with allure.step("Проверить схему JSON-ответа и данные"):
        response_json = response.json()
        creation_date = response_json['createdAt'].replace('T', ' ')
        current_date = str(datetime.datetime.utcnow())

        validate(response_json, CREATE_USER_SCHEME)
        assert response_json['name'] == body['name']
        assert creation_date[0:14] == current_date[0:14]

