"""
Базовый класс для HTTP-клиента.
Реализует общую логику отправки запросов.
"""

import requests
from typing import Dict, Any, Optional
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseAPI:
    """
    Базовый класс для API клиентов (Page Object основа).

    Attributes:
        base_url: Базовый URL API
        session: Сессия requests для переиспользования соединений
        headers: Заголовки по умолчанию

    Example:
        >>> api = BaseAPI("https://api.example.com/v1")
        >>> response = api.get("/operators")
        >>> api.close()
    """

    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        """
        Инициализация базового API клиента.

        Args:
            base_url: Базовый URL API (например, https://api.example.com/v1/)
            headers: Дополнительные заголовки по умолчанию
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

        # Базовые заголовки
        self._default_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        if headers:
            self._default_headers.update(headers)

        self.session.headers.update(self._default_headers)
        logger.info(f"BaseAPI initialized with base_url: {self.base_url}")

    def _build_url(self, endpoint: str) -> str:
        """
        Формирует полный URL из базового и endpoint.

        Args:
            endpoint: Путь к endpoint (например, /operators)

        Returns:
            Полный URL
        """
        endpoint = endpoint.lstrip('/')
        return f"{self.base_url}/{endpoint}"

    def _send_request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> requests.Response:
        """
        Отправляет HTTP-запрос.

        Args:
            method: HTTP метод (GET, POST, PUT, DELETE, PATCH)
            endpoint: Путь к endpoint
            **kwargs: Дополнительные параметры для requests

        Returns:
            Response объект

        Raises:
            requests.exceptions.HTTPError: При HTTP ошибках
            requests.exceptions.RequestException: При сетевых ошибках
        """
        url = self._build_url(endpoint)

        logger.info(f"Отправка {method} запроса на {url}")

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            logger.info(f"Успешный ответ: {response.status_code}")
            return response
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP ошибка: {e.response.status_code} - {e.response.text}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка запроса: {str(e)}")
            raise

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Выполняет GET-запрос.

        Args:
            endpoint: Путь к endpoint
            params: Query-параметры
            **kwargs: Дополнительные параметры

        Returns:
            Response объект
        """
        return self._send_request('GET', endpoint, params=params, **kwargs)

    def post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        **kwargs
    ) -> requests.Response:
        """
        Выполняет POST-запрос.

        Args:
            endpoint: Путь к endpoint
            json: JSON-тело запроса
            data: Тело запроса (для форм)
            **kwargs: Дополнительные параметры

        Returns:
            Response объект
        """
        return self._send_request('POST', endpoint, json=json, data=data, **kwargs)

    def put(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Выполняет PUT-запрос.

        Args:
            endpoint: Путь к endpoint
            json: JSON-тело запроса
            **kwargs: Дополнительные параметры

        Returns:
            Response объект
        """
        return self._send_request('PUT', endpoint, json=json, **kwargs)

    def patch(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Выполняет PATCH-запрос.

        Args:
            endpoint: Путь к endpoint
            json: JSON-тело запроса
            **kwargs: Дополнительные параметры

        Returns:
            Response объект
        """
        return self._send_request('PATCH', endpoint, json=json, **kwargs)

    def delete(
        self,
        endpoint: str,
        **kwargs
    ) -> requests.Response:
        """
        Выполняет DELETE-запрос.

        Args:
            endpoint: Путь к endpoint
            **kwargs: Дополнительные параметры

        Returns:
            Response объект
        """
        return self._send_request('DELETE', endpoint, **kwargs)

    def close(self) -> None:
        """Закрывает сессию."""
        logger.info("Закрытие HTTP сессии")
        self.session.close()

    def __enter__(self):
        """Контекстный менеджер вход."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Контекстный менеджер выход."""
        self.close()
