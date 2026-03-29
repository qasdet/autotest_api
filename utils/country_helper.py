"""
Вспомогательный класс для работы со странами.
"""

from typing import Dict, Any, List, Optional


class CountryHelper:
    """
    Вспомогательный класс для работы с данными стран.

    Предоставляет удобные методы для получения ID стран
    без прямого вызова API в тестах.
    """

    def __init__(self, country_page):
        """
        Инициализация с Page Object стран.

        Args:
            country_page: CountryPage объект
        """
        self.page = country_page
        self._cache: Optional[Dict[str, int]] = None

    def get_country_id_map(self) -> Dict[str, int]:
        """
        Получает карту всех стран {код: ID}.

        Returns:
            Словарь кодов стран и их ID
        """
        if self._cache is None:
            self._cache = self.page.get_all_ids()
        return self._cache

    def get_id(self, country_code: str) -> Optional[int]:
        """
        Получает ID страны по коду.

        Args:
            country_code: Код страны

        Returns:
            ID страны или None
        """
        return self.get_country_id_map().get(country_code)

    def get_russia_id(self) -> Optional[int]:
        """Возвращает ID России."""
        return self.get_id('RUS')

    def get_korea_id(self) -> Optional[int]:
        """Возвращает ID Кореи."""
        return self.get_id('KOR')

    def get_moldova_id(self) -> Optional[int]:
        """Возвращает ID Молдовы."""
        return self.get_id('MDA')

    def get_ids_dict(self) -> Dict[str, Any]:
        """
        Возвращает словарь с ID стран в формате для payload.

        Returns:
            Словарь с ключами rus_id, kor_id, mld_id
        """
        country_map = self.get_country_id_map()
        return {
            'rus_id': country_map.get('RUS'),
            'kor_id': country_map.get('KOR'),
            'mld_id': country_map.get('MDA')
        }

    def clear_cache(self) -> None:
        """Очищает кэш стран."""
        self._cache = None
