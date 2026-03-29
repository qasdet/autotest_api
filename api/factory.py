"""
Page Factory для создания API объектов.

Реализует паттерн Factory для централизованного создания
и управления Page Object'ами.
"""

from typing import Type, TypeVar, Dict, Optional
import logging

from api.base_api import BaseAPI
from api.page_objects.operator_page import OperatorPage
from api.page_objects.country_page import CountryPage

T = TypeVar('T', bound=BaseAPI)
logger = logging.getLogger(__name__)


class APIFactory:
    """
    Фабрика для создания Page Object'ов (API Factory Pattern).

    Паттерн Factory обеспечивает:
    - Централизованное создание API объектов
    - Кэширование экземпляров (один объект = одна сессия HTTP)
    - Управление жизненным циклом объектов
    - Ленивую инициализацию

    Example:
        >>> factory = APIFactory("https://api.example.com/v1")
        >>> operator_page = factory.get_operator_page()
        >>> country_page = factory.get_country_page()
        >>> factory.close_all()  # Закрыть все сессии

        # Или через контекстный менеджер:
        >>> with APIFactory(base_url) as factory:
        ...     operator_page = factory.get_operator_page()
    """

    def __init__(
        self,
        base_url: str,
        default_headers: Optional[Dict[str, str]] = None
    ):
        """
        Инициализация Page Factory.

        Args:
            base_url: Базовый URL API
            default_headers: Заголовки по умолчанию для всех объектов
        """
        self.base_url = base_url
        self.default_headers = default_headers or {}
        self._cache: Dict[str, BaseAPI] = {}
        logger.info(f"APIFactory initialized for {base_url}")

    def _get_or_create(
        self,
        key: str,
        page_class: Type[T],
        *args,
        **kwargs
    ) -> T:
        """
        Получает объект из кэша или создает новый.

        Args:
            key: Ключ для кэша
            page_class: Класс Page Object
            *args: Позиционные аргументы для конструктора
            **kwargs: Именованные аргументы для конструктора

        Returns:
            Экземпляр Page Object
        """
        if key not in self._cache:
            logger.info(f"Создание нового Page Object: {page_class.__name__}")

            # Создаем объект с базовым URL и заголовками
            obj = page_class(
                self.base_url,
                headers=self.default_headers,
                *args,
                **kwargs
            )
            self._cache[key] = obj
        else:
            logger.debug(f"Возвращен кэшированный Page Object: {key}")

        return self._cache[key]

    def get_operator_page(self) -> OperatorPage:
        """
        Создает или возвращает кэшированный OperatorPage.

        Returns:
            OperatorPage объект для работы с /operators
        """
        return self._get_or_create('operator', OperatorPage)

    def get_country_page(self) -> CountryPage:
        """
        Создает или возвращает кэшированный CountryPage.

        Returns:
            CountryPage объект для работы с /countries
        """
        return self._get_or_create('country', CountryPage)

    def get_custom_page(
        self,
        page_class: Type[T],
        key: Optional[str] = None,
        *args,
        **kwargs
    ) -> T:
        """
        Создает произвольный Page Object.

        Args:
            page_class: Класс Page Object
            key: Ключ для кэша (если None, используется имя класса)
            *args: Аргументы для конструктора
            **kwargs: Именованные аргументы

        Returns:
            Экземпляр кастомного Page Object
        """
        cache_key = key or page_class.__name__
        return self._get_or_create(cache_key, page_class, *args, **kwargs)

    def clear_cache(self) -> None:
        """Очищает кэш Page Objects без закрытия сессий."""
        logger.info("Очистка кэша Page Objects")
        self._cache.clear()

    def close_all(self) -> None:
        """
        Закрывает все HTTP сессии и очищает кэш.

        Должен вызываться при завершении работы с фабрикой
        для освобождения ресурсов.
        """
        logger.info(f"Закрытие {len(self._cache)} Page Objects")
        for key, page_obj in self._cache.items():
            try:
                page_obj.close()
                logger.debug(f"Закрыт {key}")
            except Exception as e:
                logger.error(f"Ошибка при закрытии {key}: {e}")
        self._cache.clear()

    def __enter__(self):
        """Контекстный менеджер вход."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Контекстный менеджер выход с автоматическим закрытием."""
        self.close_all()

    def __del__(self):
        """Деструктор - пытается закрыть сессии при удалении."""
        if self._cache:
            self.close_all()
