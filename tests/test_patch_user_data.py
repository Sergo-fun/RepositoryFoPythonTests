import datetime
import allure
import httpx
from jsonschema import validate
from core.contracts import UPDATE_USER_SCHEME

BASE_URL = "https://reqres.in/"
UPDATE_USER = "api/users/2"

@allure.suite("PUT User API")
@allure.title("Создание пользователя с корректными данными")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_user():
    body = {
        "name": "morpheuuuus",
        "job": "leader"
    }
    with allure.step("Отправить PUT-запрос для обновления данных пользователя"):
        response = httpx.patch(BASE_URL + UPDATE_USER, json=body)

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 200

    with allure.step("Проверить схему JSON-ответа и данные"):
        response_json = response.json()
        updation_date = response_json['updatedAt'].replace('T', ' ')
        current_date = str(datetime.datetime.utcnow())

        validate(response_json, UPDATE_USER_SCHEME)
        assert response_json['name'] == body['name']
        assert response_json['job'] == body['job']
        assert updation_date[0:14] == current_date[0:14]
