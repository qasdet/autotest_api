"""
Page Object для API стран.

Инкапсулирует операции со справочником стран,
которые необходимы для получения countryId при создании операторов.
"""

from typing import Dict, Any, Optional, List
import requests

from api.page_objects.base_page import BasePage


class CountryPage(BasePage):
    """
    Page Object для работы с API стран.

    Предоставляет методы для получения информации о странах
    и их ID, которые требуются для создания операторов.

    Example:
        >>> page = CountryPage("https://api.example.com/v1")
        >>> # Получение всех стран
        >>> response = page.get_all()
        >>> # Получение по коду
        >>> country_id = page.get_id_by_code('RUS')  # → 1
        >>> # Получение по ID
        >>> response = page.get_by_id(1)
    """

    RESOURCE = "countries"

    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        """
        Инициализация CountryPage.

        Args:
            base_url: Базовый URL API
            headers: Дополнительные заголовки
        """
        super().__init__(base_url, headers, self.RESOURCE)

    # ═══════════════════════════════════════════════════
    # READ операции
    # ═══════════════════════════════════════════════════

    def get_all(self, **kwargs) -> requests.Response:
        """
        Получает список всех стран.

        Args:
            **kwargs: Дополнительные параметры запроса

        Returns:
            Response объект со списком стран
        """
        return self.get(self._resource_url(), **kwargs)

    def get_by_id(
        self,
        country_id: int,
        **kwargs
    ) -> requests.Response:
        """
        Получает страну по ID.

        Args:
            country_id: ID страны
            **kwargs: Дополнительные параметры запроса

        Returns:
            Response объект с данными страны
        """
        return self.get(self._resource_url(str(country_id)), **kwargs)

    def get_by_code(
        self,
        country_code: str,
        **kwargs
    ) -> requests.Response:
        """
        Получает страну по коду (ISO 3166-1 alpha-3).

        Args:
            country_code: Код страны (например, 'RUS')
            **kwargs: Дополнительные параметры

        Returns:
            Response объект с данными страны
        """
        return self.get_all(
            params={"countryCode": country_code},
            **kwargs
        )

    # ═══════════════════════════════════════════════════
    # Вспомогательные методы
    # ═══════════════════════════════════════════════════

    def get_id_by_code(
        self,
        country_code: str,
        **kwargs
    ) -> Optional[int]:
        """
        Получает ID страны по её коду.

        Выполняет GET /countries и ищет страну с указанным кодом.

        Args:
            country_code: Код страны (ISO 3166-1 alpha-3)

        Returns:
            ID страны или None, если не найдена
        """
        response = self.get_all(**kwargs)
        data = response.json()

        # Поддержка разных структур ответа
        items = data.get('items', []) or data.get('countries', []) or data

        if isinstance(items, dict):
            items = [items]

        for item in items:
            if item.get('countryCode') == country_code:
                return item.get('countryId') or item.get('id')

        return None

    def get_ids_by_codes(
        self,
        country_codes: List[str]
    ) -> Dict[str, Optional[int]]:
        """
        Получает ID нескольких стран по их кодам.

        Args:
            country_codes: Список кодов стран

        Returns:
            Словарь {код страны: ID или None}
        """
        return {
            code: self.get_id_by_code(code)
            for code in country_codes
        }

    def get_all_ids(self) -> Dict[str, int]:
        """
        Получает словарь всех доступных стран {код: ID}.

        Returns:
            Словарь {код страны: ID}
        """
        response = self.get_all()
        data = response.json()

        # Поддержка разных структур ответа
        items = data.get('items', []) or data.get('countries', []) or data

        if isinstance(items, dict):
            items = [items]

        return {
            item['countryCode']: item.get('countryId') or item.get('id')
            for item in items
            if 'countryCode' in item
        }

    def get_country_codes(self) -> List[str]:
        """
        Получает список всех кодов стран.

        Returns:
            Список кодов стран
        """
        return list(self.get_all_ids().keys())

    def get_country_info(
        self,
        country_code: str
    ) -> Optional[Dict[str, Any]]:
        """
        Получает полную информацию о стране по коду.

        Args:
            country_code: Код страны

        Returns:
            Данные страны или None
        """
        response = self.get_by_code(country_code)
        data = response.json()

        items = data.get('items', []) or data.get('countries', [])

        if isinstance(items, list):
            for item in items:
                if item.get('countryCode') == country_code:
                    return item
        elif isinstance(items, dict) and items.get('countryCode') == country_code:
            return items

        return None

    def country_exists(self, country_code: str) -> bool:
        """
        Проверяет существование страны.

        Args:
            country_code: Код страны

        Returns:
            True если страна существует
        """
        return self.get_id_by_code(country_code) is not None
