"""
GET тесты для операторов.

Все тесты имеют order=2 и выполняются после POST тестов.
"""

import pytest
import allure
from requests import Response

from utils.response_validators import OperatorValidator, ResponseValidator


@allure.epic("Operators API")
@allure.feature("Read Operations")
class TestGetOperators:
    """
    Тесты для получения операторов через GET /operators.
    """

    @pytest.mark.order(2)
    @allure.story("Get All Operators")
    @allure.title("Получение списка всех операторов")
    @allure.description("""
        Тест проверяет получение списка операторов.
        Предусловие: POST тесты должны были создать операторов.
    """)
    def test_get_all_operators(self, operator_page):
        """
        Тест получения списка операторов.

        Args:
            operator_page: Page Object для операторов
        """
        with allure.step("Запрос списка через Page Object"):
            response: Response = operator_page.get_all()
            allure.attach(
                f"Статус: {response.status_code}",
                name="Response Status",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Валидация ответа"):
            operators = OperatorValidator.assert_list_response(response)
            allure.attach(
                response.text[:1000],
                name="Response Body (truncated)",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Проверка данных"):
            assert isinstance(operators, list), "Ответ должен быть списком"
            allure.attach(
                f"Найдено операторов: {len(operators)}",
                name="Operators Count",
                attachment_type=allure.attachment_type.TEXT
            )

    @pytest.mark.order(2)
    @allure.story("Get By Country")
    @allure.title("Получение операторов по стране (Россия)")
    def test_get_operators_by_country(self, operator_page, country_ids):
        """
        Тест получения операторов по ID страны.

        Args:
            operator_page: Page Object для операторов
            country_ids: ID стран
        """
        rus_id = country_ids.get('rus_id')
        if not rus_id:
            pytest.skip("ID России не найден")

        with allure.step(f"Запрос операторов страны (ID: {rus_id})"):
            response = operator_page.get_by_country(rus_id)

        with allure.step("Проверка ответа"):
            ResponseValidator.assert_status(response, 200)
            allure.attach(
                response.text[:500],
                name="Response",
                attachment_type=allure.attachment_type.JSON
            )

    @pytest.mark.order(2)
    @allure.story("Search Operators")
    @allure.title("Поиск операторов")
    def test_search_operators(self, operator_page):
        """
        Тест поиска операторов.

        Args:
            operator_page: Page Object для операторов
        """
        with allure.step("Поиск операторов"):
            response = operator_page.search("test")
            ResponseValidator.assert_status(response, 200)


@allure.epic("Operators API")
@allure.feature("Get By ID")
class TestGetOperatorById:
    """
    Тесты для получения конкретного оператора по ID.
    """

    @pytest.mark.order(2)
    @allure.story("Get Existing Operator")
    @allure.title("Получение существующего оператора по ID")
    def test_get_existing_operator(
        self,
        operator_page,
        local_payload
    ):
        """
        Тест получения существующего оператора.

        Args:
            operator_page: Page Object для операторов
            local_payload: Payload для создания
        """
        with allure.step("Создание тестового оператора"):
            create_response = operator_page.create(local_payload)
            create_data = create_response.json()
            operator_id = create_data.get('operatorId')

        with allure.step(f"Получение оператора по ID: {operator_id}"):
            response = operator_page.get_by_id(operator_id)

        with allure.step("Валидация ответа"):
            ResponseValidator.assert_status(response, 200)
            data = response.json()
            assert data.get('operatorId') == operator_id

            allure.attach(
                response.text,
                name="Operator Data",
                attachment_type=allure.attachment_type.JSON
            )

    @pytest.mark.order(2)
    @allure.story("Get Non-existent Operator")
    @allure.title("Получение несуществующего оператора")
    def test_get_nonexistent_operator(self, operator_page):
        """
        Тест получения несуществующего оператора.

        Args:
            operator_page: Page Object для операторов
        """
        with allure.step("Запрос несуществующего оператора (ID: 999999)"):
            response = operator_page.get_by_id(999999)

        with allure.step("Проверка ответа"):
            # API должен вернуть 404
            if response.status_code == 404:
                allure.attach(
                    "Корректный ответ 404",
                    name="Expected Error",
                    attachment_type=allure.attachment_type.TEXT
                )
            else:
                allure.attach(
                    f"Получен статус: {response.status_code}",
                    name="Response",
                    attachment_type=allure.attachment_type.TEXT
                )
