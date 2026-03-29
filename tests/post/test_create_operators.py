"""
POST тесты для создания операторов.

Все тесты в этом пакете имеют order=1 и выполняются первыми.
Используют Page Object паттерн через фикстуры.
"""

import pytest
import allure
from requests import Response

from utils.response_validators import OperatorValidator, ResponseValidator


@allure.epic("Operators API")
@allure.feature("Create Operations")
class TestCreateOperators:
    """
    Тесты для создания операторов через POST /operators.
    Использует Page Object паттерн для абстракции от HTTP.
    """

    @pytest.mark.order(1)
    @allure.story("Create Single Operator")
    @allure.title("Создание локального оператора (Россия)")
    @allure.description("""
        Тест проверяет создание оператора с локальными данными.
        Страна: Россия (RUS).
        Ожидается статус 201 и возврат созданного оператора.
    """)
    def test_create_local_operator(self, operator_page, local_payload):
        """
        Тест создания локального оператора.

        Args:
            operator_page: Page Object для операторов
            local_payload: Payload для локального оператора
        """
        with allure.step("Отправка POST запроса через Page Object"):
            response: Response = operator_page.create(local_payload)
            allure.attach(
                str(local_payload),
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Валидация ответа"):
            data = OperatorValidator.assert_created(response)
            allure.attach(
                response.text,
                name="Response",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Проверка данных в ответе"):
            country = data.get('country', {})
            assert country.get('countryName') == "Russia", (
                "Должна быть страна Russia"
            )

    @pytest.mark.order(1)
    @allure.story("Create Single Operator")
    @allure.title("Создание praqe оператора (Молдова)")
    def test_create_praqe_operator(self, operator_page, praqe_payload):
        """
        Тест создания praqe оператора.

        Args:
            operator_page: Page Object для операторов
            praqe_payload: Payload для praqe оператора
        """
        with allure.step("Создание оператора"):
            response = operator_page.create(praqe_payload)
            data = OperatorValidator.assert_created(response)

        with allure.step("Проверка данных"):
            country = data.get('country', {})
            assert country.get('countryName') == "Moldova", (
                "Должна быть страна Moldova"
            )

    @pytest.mark.order(1)
    @pytest.mark.parametrize("payload", [
        "local_payload",
        "praqe_payload"
    ])
    @allure.story("Create Multiple Operators")
    @allure.title("Создание оператора: {payload}")
    def test_create_operators_parametrized(
        self,
        operator_page,
        payload: str,
        request
    ):
        """
        Параметризованный тест создания операторов.

        Создает операторов с разными payload.

        Args:
            operator_page: Page Object для операторов
            payload: Имя фикстуры с payload
            request: Объект pytest для получения фикстур
        """
        # Получаем payload по имени
        actual_payload = request.getfixturevalue(payload)

        with allure.step(f"Создание оператора с payload: {payload}"):
            response = operator_page.create(actual_payload)
            data = OperatorValidator.assert_created(response)

        with allure.step("Проверка наличия ID"):
            assert data.get('operatorId') is not None
            allure.attach(
                f"Создан оператор с ID: {data.get('operatorId')}",
                name="Created Operator ID",
                attachment_type=allure.attachment_type.TEXT
            )

    @pytest.mark.order(1)
    @allure.story("Create and Verify")
    @allure.title("E2E: Создание и проверка оператора")
    def test_create_and_verify(self, operator_page, local_payload):
        """
        E2E тест: создание и последующая проверка.

        Демонстрирует использование Page Object для цепочки:
        POST → GET

        Args:
            operator_page: Page Object для операторов
            local_payload: Payload для оператора
        """
        with allure.step("1. Создание оператора (POST)"):
            create_response = operator_page.create(local_payload)
            create_data = OperatorValidator.assert_created(create_response)
            operator_id = create_data.get('operatorId')

            allure.attach(
                f"ID созданного оператора: {operator_id}",
                name="Created ID",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("2. Получение оператора (GET)"):
            get_response = operator_page.get_by_id(operator_id)
            get_data = get_response.json()

            allure.attach(
                get_response.text,
                name="GET Response",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("3. Сравнение данных"):
            assert get_data.get('operatorId') == operator_id, (
                "ID из GET должен совпадать с ID созданного"
            )


@allure.epic("Operators API")
@allure.feature("Negative Cases")
class TestCreateOperatorsNegative:
    """
    Негативные тесты для создания операторов.
    """

    @pytest.mark.order(1)
    @allure.story("Invalid Payload")
    @allure.title("Создание с невалидным payload")
    def test_create_with_invalid_payload(self, operator_page):
        """
        Тест создания с невалидными данными.

        Args:
            operator_page: Page Object для операторов
        """
        invalid_payload = {
            "col1": "test"
            # Отсутствует обязательное поле country
        }

        with allure.step("Попытка создания с невалидным payload"):
            try:
                response = operator_page.create(invalid_payload)
                allure.attach(
                    f"Получен статус: {response.status_code}",
                    name="Response",
                    attachment_type=allure.attachment_type.TEXT
                )
                # API может вернуть 400 или другой статус
            except Exception as e:
                allure.attach(
                    f"Ошибка: {str(e)}",
                    name="Error",
                    attachment_type=allure.attachment_type.TEXT
                )
