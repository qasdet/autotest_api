"""
Page Object для API операторов.

Предоставляет интерфейс для работы со всеми операциями CRUD
над ресурсом /operators.
"""

from typing import Dict, Any, Optional, List
import requests

from api.page_objects.base_page import BasePage


class OperatorPage(BasePage):
    """
    Page Object для работы с API операторов.

    Инкапсулирует все операции со эндпоинтом /operators:
    - CREATE: POST /operators
    - READ: GET /operators, GET /operators/{id}
    - UPDATE: PUT /operators/{id}
    - DELETE: DELETE /operators/{id}

    Example:
        >>> page = OperatorPage("https://api.example.com/v1")
        >>> # Создание
        >>> response = page.create({"name": "Test", "countryId": 1})
        >>> # Получение списка
        >>> response = page.get_all()
        >>> # Получение по ID
        >>> response = page.get_by_id(123)
        >>> # Обновление
        >>> response = page.update(123, {"name": "Updated"})
        >>> # Удаление
        >>> response = page.delete(123)
    """

    RESOURCE = "operators"

    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        """
        Инициализация OperatorPage.

        Args:
            base_url: Базовый URL API
            headers: Дополнительные заголовки
        """
        super().__init__(base_url, headers, self.RESOURCE)

    # ═══════════════════════════════════════════════════
    # CREATE операции
    # ═══════════════════════════════════════════════════

    def create(
        self,
        data: Dict[str, Any],
        **kwargs
    ) -> requests.Response:
        """
        Создает нового оператора.

        Args:
            data: Данные оператора для создания
            **kwargs: Дополнительные параметры запроса

        Returns:
            Response объект с созданным оператором
        """
        return self.post(self._resource_url(), json=data, **kwargs)

    # ═══════════════════════════════════════════════════
    # READ операции
    # ═══════════════════════════════════════════════════

    def get_all(
        self,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Получает список всех операторов.

        Args:
            params: Query-параметры для фильтрации
            **kwargs: Дополнительные параметры запроса

        Returns:
            Response объект со списком операторов
        """
        return self.get(self._resource_url(), params=params, **kwargs)

    def get_by_id(
        self,
        operator_id: int,
        **kwargs
    ) -> requests.Response:
        """
        Получает оператора по ID.

        Args:
            operator_id: ID оператора
            **kwargs: Дополнительные параметры запроса

        Returns:
            Response объект с данными оператора
        """
        return self.get(self._resource_url(str(operator_id)), **kwargs)

    def get_by_country(
        self,
        country_id: int,
        **kwargs
    ) -> requests.Response:
        """
        Получает операторов по ID страны.

        Args:
            country_id: ID страны
            **kwargs: Дополнительные параметры запроса

        Returns:
            Response объект со списком операторов страны
        """
        return self.get_all(params={"countryId": country_id}, **kwargs)

    def search(
        self,
        query: str,
        **kwargs
    ) -> requests.Response:
        """
        Ищет операторов по запросу.

        Args:
            query: Поисковый запрос
            **kwargs: Дополнительные параметры запроса

        Returns:
            Response объект с результатами поиска
        """
        return self.get_all(params={"search": query}, **kwargs)

    # ═══════════════════════════════════════════════════
    # UPDATE операции
    # ═══════════════════════════════════════════════════

    def update(
        self,
        operator_id: int,
        data: Dict[str, Any],
        **kwargs
    ) -> requests.Response:
        """
        Полностью обновляет оператора (PUT).

        Args:
            operator_id: ID оператора
            data: Новые данные оператора
            **kwargs: Дополнительные параметры запроса

        Returns:
            Response объект с обновленным оператором
        """
        return self.put(
            self._resource_url(str(operator_id)),
            json=data,
            **kwargs
        )

    def partial_update(
        self,
        operator_id: int,
        data: Dict[str, Any],
        **kwargs
    ) -> requests.Response:
        """
        Частично обновляет оператора (PATCH).

        Args:
            operator_id: ID оператора
            data: Данные для частичного обновления
            **kwargs: Дополнительные параметры запроса

        Returns:
            Response объект с обновленным оператором
        """
        return self.patch(
            self._resource_url(str(operator_id)),
            json=data,
            **kwargs
        )

    # ═══════════════════════════════════════════════════
    # DELETE операции
    # ═══════════════════════════════════════════════════

    def delete(
        self,
        operator_id: int,
        **kwargs
    ) -> requests.Response:
        """
        Удаляет оператора.

        Args:
            operator_id: ID оператора
            **kwargs: Дополнительные параметры запроса

        Returns:
            Response объект с результатом удаления
        """
        return self.delete(self._resource_url(str(operator_id)), **kwargs)

    # ═══════════════════════════════════════════════════
    # Вспомогательные методы
    # ═══════════════════════════════════════════════════

    def exists(self, operator_id: int) -> bool:
        """
        Проверяет существование оператора.

        Args:
            operator_id: ID оператора

        Returns:
            True если оператор существует, иначе False
        """
        try:
            response = self.get_by_id(operator_id)
            return response.status_code == 200
        except Exception:
            return False

    def get_id_by_name(
        self,
        name: str,
        **kwargs
    ) -> Optional[int]:
        """
        Получает ID оператора по имени.

        Args:
            name: Имя оператора
            **kwargs: Дополнительные параметры

        Returns:
            ID оператора или None
        """
        response = self.search(name, **kwargs)
        data = response.json()

        items = data.get('items', [])
        for item in items:
            if item.get('name') == name:
                return item.get('operatorId') or item.get('id')

        return None
