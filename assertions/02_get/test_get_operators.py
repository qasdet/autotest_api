import pytest
import allure


@pytest.mark.order(2)  # GET тесты выполняются после POST
@allure.feature("Operators API")
@allure.story("Get Operators")
@allure.title("Get operators list")
def test_get_operators(get_operators):
    with allure.step("Send GET request to get operators list"):
        response = get_operators.get_operators()

    with allure.step("Verify response status code is 200"):
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()

    with allure.step("Attach response data"):
        allure.attach(str(data), name="Response Body", attachment_type=allure.attachment_type.JSON)

    with allure.step("Verify response contract"):
        # assert_get_operators(data)  # Раскомментировать после реализации функции
        allure.step("Contract validation skipped - implement assert_get_operators() in assertions.py")