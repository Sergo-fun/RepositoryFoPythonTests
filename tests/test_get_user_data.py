import httpx
from jsonschema import validate

from core.contracts import USER_DATA_SCHEME , COLOR_DATA_SCHEME

BASE_URL = "https://reqres.in/"
LIST_USERS = "api/users?page=2"
EMAIL_ENDS = "@reqres.in"
AVATAR_ENDS = "-image.jpg"
SINGLE_USER = "api/users/2"
NOT_FOUND_USER = "api/users/23"
LIST_RESOURCES = "api/unknown"
SINGLE_RESOURCE = "api/unknown/2"
NOT_FOUND_RESOURCE = "api/unknown/23"
def test_list_users():
    response = httpx.get(BASE_URL + LIST_USERS)
    assert response.status_code == 200
    data = response.json()['data']

    for item in data:
        validate(item, USER_DATA_SCHEME)
        assert item['email'].endswith(EMAIL_ENDS)
        assert item['avatar'].endswith(str(item['id']) + AVATAR_ENDS)

def test_single_user():
    response = httpx.get(BASE_URL + SINGLE_USER)
    assert response.status_code == 200
    data = response.json()['data']

    assert data['email'].endswith(EMAIL_ENDS)
    assert data['avatar'].endswith(str(data['id']) + AVATAR_ENDS)

def test_user_not_found():
        response = httpx.get(BASE_URL + NOT_FOUND_USER)
        assert response.status_code == 404
def test_list_colors():
    response = httpx.get(BASE_URL + LIST_RESOURCES)
    assert response.status_code == 200

    data = response.json()['data']
    assert isinstance(data, list)
    assert len(data) > 0

    for item in data:
        validate(item, COLOR_DATA_SCHEME)
        assert item['year'] >= 2000
        assert item['color'].startswith('#')


def test_single_colors():
    response = httpx.get(BASE_URL + SINGLE_RESOURCE)
    assert response.status_code == 200

    data = response.json()['data']
    validate(data, COLOR_DATA_SCHEME)
    assert data['id'] == 2
    assert data['name'] == "fuchsia rose"
    assert data['color'] == "#C74375"


def test_user_not_found_resources():
    response = httpx.get(BASE_URL + NOT_FOUND_RESOURCE)
    assert response.status_code == 404


