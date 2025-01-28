import allure
import httpx

BASE_URL = "https://reqres.in/"
DELETE_USER = "api/users/2"
GET_USER = "api/users/2"


@allure.suite("DELETE User API")
@allure.title("Удаление пользователя с корректным запросом")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_user():
    with allure.step("Отправить DELETE-запрос для удаления пользователя"):
        response = httpx.delete(BASE_URL + DELETE_USER)

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 204

    with allure.step("Попытка удалить несуществующего пользователя"):
        response = httpx.delete(BASE_URL + "api/users/999")
        assert response.status_code == 204


