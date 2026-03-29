"""
Базовый класс для Page Objects.
"""

from typing import Dict, Any, Optional
from api.base_api import BaseAPI


class BasePage(BaseAPI):
    """
    Базовый класс для всех Page Objects.

    Добавляет общую функциональность для работы с API ресурсами.
    """

    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        resource_path: str = ""
    ):
        """
        Инициализация базового Page Object.

        Args:
            base_url: Базовый URL
            headers: Заголовки
            resource_path: Путь к ресурсу (например, /operators)
        """
        super().__init__(base_url, headers)
        self.resource_path = resource_path

    def _resource_url(self, resource_id: Optional[str] = None) -> str:
        """
        Формирует URL к ресурсу.

        Args:
            resource_id: ID ресурса (опционально)

        Returns:
            Полный путь к ресурсу
        """
        if resource_id:
            return f"{self.resource_path}/{resource_id}"
        return self.resource_path
