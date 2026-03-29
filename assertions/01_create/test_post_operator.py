import pytest
import allure


@pytest.mark.order(1)  # POST тесты выполняются первыми
@pytest.mark.parametrize("all_operator", [
    "oper_local_payload",
    "oper_praqe_payload"
])
@allure.feature("Operators API")
@allure.story("Create Operators")
@allure.title("Create operator with {all_operator}")
def test_post_broker(create_oper, all_operator, oper_local_payload, oper_praqe_payload):
    payloads = {
        "oper_local_payload": oper_local_payload,
        "oper_praqe_payload": oper_praqe_payload
    }

    oper_data = payloads[all_operator]

    with allure.step(f"Send POST request to create operator with {all_operator}"):
        response = create_oper.create_operator(oper_data)

    with allure.step("Verify response status code is 200 or 201"):
        assert response.status_code in [200, 201], f"Expected 200 or 201, got {response.status_code}"

    with allure.step("Attach request and response details"):
        allure.attach(str(oper_data), name="Request Payload", attachment_type=allure.attachment_type.JSON)
        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)