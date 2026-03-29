import pytest

@pytest.mark.parametrize("all_operator", [
    "oper_local_payload",
    "oper_praqe_payload"
])

def test_post_broker(create_oper,all_operator,oper_local_payload,oper_praqe_payload):
    payloads = {
        "oper_local_payload" : oper_local_payload,
        "oper_praqe_payload" : oper_praqe_payload
    }

    oper_data = payloads[all_operator]

    response = create_oper.create_operator(oper_data)

    assert response.status_code == 200 or response.status_code == 201