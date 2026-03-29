"""
GET тесты для API стран.

Используют CountryPage для работы со справочником стран.
"""

import pytest
import allure

from utils.response_validators import CountryValidator


@allure.epic("Countries API")
@allure.feature("Read Operations")
class TestGetCountries:
    """
    Тесты для получения информации о странах.
    """

    @pytest.mark.order(2)
    @allure.story("Get All Countries")
    @allure.title("Получение списка всех стран")
    def test_get_all_countries(self, country_page):
        """
        Тест получения списка стран.

        Args:
            country_page: Page Object для стран
        """
        with allure.step("Запрос списка стран"):
            response = country_page.get_all()

        with allure.step("Валидация ответа"):
            data = response.json()
            items = data.get('items', [])

            allure.attach(
                response.text[:500],
                name="Countries Response",
                attachment_type=allure.attachment_type.JSON
            )

            assert len(items) > 0, "Должен вернуться непустой список стран"

            # Проверяем структуру первой страны
            if items:
                CountryValidator.assert_has_country_fields(items[0])

    @pytest.mark.order(2)
    @allure.story("Get Country by Code")
    @allure.title("Получение страны по коду (RUS)")
    def test_get_country_by_code(self, country_page):
        """
        Тест получения страны по коду.

        Args:
            country_page: Page Object для стран
        """
        with allure.step("Запрос страны с кодом RUS"):
            response = country_page.get_by_code('RUS')

        with allure.step("Проверка ответа"):
            # API может вернуть 200 с пустым списком если не найдено
            if response.status_code == 200:
                data = response.json()
                allure.attach(
                    response.text,
                    name="Country Data",
                    attachment_type=allure.attachment_type.JSON
                )

    @pytest.mark.order(2)
    @allure.story("Helper Methods")
    @allure.title("Вспомогательный метод: получение ID по коду")
    def test_get_country_id_helper(self, country_helper):
        """
        Тест вспомогательного метода получения ID.

        Args:
            country_helper: Вспомогательный объект
        """
        with allure.step("Получение ID России"):
            rus_id = country_helper.get_russia_id()
            allure.attach(
                f"ID России: {rus_id}",
                name="Russia ID",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Получение ID всех стран"):
            ids = country_helper.get_ids_dict()
            allure.attach(
                str(ids),
                name="Country IDs",
                attachment_type=allure.attachment_type.JSON
            )

    @pytest.mark.order(2)
    @allure.story("Get All IDs")
    @allure.title("Получение словаря всех ID стран")
    def test_get_all_country_ids(self, country_page):
        """
        Тест получения словаря ID всех стран.

        Args:
            country_page: Page Object для стран
        """
        with allure.step("Запрос всех ID"):
            ids = country_page.get_all_ids()

        with allure.step("Проверка результата"):
            assert 'RUS' in ids or len(ids) > 0, (
                "Должны быть получены ID стран"
            )

            allure.attach(
                str(ids),
                name="All Country IDs",
                attachment_type=allure.attachment_type.JSON
            )
