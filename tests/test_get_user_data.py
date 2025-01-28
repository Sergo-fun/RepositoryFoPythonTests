import httpx
from jsonschema import validate
import allure
from core.contracts import USER_DATA_SCHEME, COLOR_DATA_SCHEME

BASE_URL = "https://reqres.in/"
LIST_USERS = "api/users?page=2"
EMAIL_ENDS = "@reqres.in"
AVATAR_ENDS = "-image.jpg"
SINGLE_USER = "api/users/2"
NOT_FOUND_USER = "api/users/23"
LIST_RESOURCES = "api/unknown"
SINGLE_RESOURCE = "api/unknown/2"
NOT_FOUND_RESOURCE = "api/unknown/23"


@allure.suite('Проверка запроса данных пользователей')
@allure.title('Проверяем получение списка пользователей')
def test_list_users():
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + LIST_USERS}'):
        response = httpx.get(BASE_URL + LIST_USERS)

    with allure.step('Проверяем код ответа'):
        assert response.status_code == 200
    data = response.json()['data']

    for item in data:
        with allure.step('Проверяем элемент из списка'):
            validate(item, USER_DATA_SCHEME)
        with allure.step('Проверяем окончание EMAIL'):
            assert item['email'].endswith(EMAIL_ENDS)
        with allure.step('Проверяем окончание AVATAR'):
            assert item['avatar'].endswith(str(item['id']) + AVATAR_ENDS)


@allure.suite('Проверка запроса данных конкретного пользователя')
@allure.title('Проверяем получение данных пользователя')
def test_single_user():
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + SINGLE_USER}'):
        response = httpx.get(BASE_URL + SINGLE_USER)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 200
    data = response.json()['data']
    with allure.step('Проверяем окончание EMAIL'):
        assert data['email'].endswith(EMAIL_ENDS)
    with allure.step('Проверяем окончание AVATAR'):
        assert data['avatar'].endswith(str(data['id']) + AVATAR_ENDS)


@allure.suite('Получение несуществующего пользователя')
def test_user_not_found():
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + NOT_FOUND_USER}'):
        response = httpx.get(BASE_URL + NOT_FOUND_USER)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 404


@allure.suite('Проверка запроса данных ресурсов ')
@allure.title('Проверяем получение списка ресурсов')
def test_list_colors():
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + LIST_RESOURCES}'):
        response = httpx.get(BASE_URL + LIST_RESOURCES)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 200

    data = response.json()['data']
    assert isinstance(data, list)
    assert len(data) > 0

    for item in data:
        with allure.step('Проверяем элемент из списка'):
            validate(item, COLOR_DATA_SCHEME)
        with allure.step('Проверяем год '):
            assert item['year'] >= 2000
        with allure.step('Проверяем цвет '):
            assert item['color'].startswith('#')


@allure.suite('Проверка запроса данных конкретного ресурса')
@allure.title('Проверяем получение данных ресурса')
def test_single_colors():
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + SINGLE_RESOURCE}'):
        response = httpx.get(BASE_URL + SINGLE_RESOURCE)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 200

    data = response.json()['data']
    validate(data, COLOR_DATA_SCHEME)
    with allure.step('Проверяем id'):
        assert data['id'] == 2
    with allure.step('Проверяем имя'):
        assert data['name'] == "fuchsia rose"
    with allure.step('Проверяем цвет'):
        assert data['color'] == "#C74375"


('Получение несуществующего ресурса')


def test_user_not_found_resources():
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + NOT_FOUND_RESOURCE}'):
        response = httpx.get(BASE_URL + NOT_FOUND_RESOURCE)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 404
