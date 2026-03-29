"""
Фикстуры pytest для тестирования.

Реализует Page Factory паттерн через фикстуры pytest.
Все API объекты создаются через фабрику и кэшируются на уровне сессии.
"""

import os
import pytest
import logging
from dotenv import load_dotenv

from api.factory import APIFactory
from api.page_objects.operator_page import OperatorPage
from api.page_objects.country_page import CountryPage
from payload.operator_payloads import (
    local_operator_payload,
    praqe_operator_payload
)
from utils.country_helper import CountryHelper

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()


# ═══════════════════════════════════════════════════
# Фикстуры конфигурации
# ═══════════════════════════════════════════════════

@pytest.fixture(scope='session')
def base_url() -> str:
    """
    Базовый URL API из переменной окружения CLIENT.

    Returns:
        URL API

    Raises:
        pytest.fail: Если CLIENT не задан
    """
    url = os.getenv('CLIENT')
    if not url:
        pytest.fail(
            "Переменная окружения CLIENT не установлена. "
            "Создайте файл .env из .env.example"
        )
    return url.rstrip('/')


@pytest.fixture(scope='session')
def api_headers() -> dict:
    """
    Заголовки по умолчанию для API запросов.

    Returns:
        Словарь заголовков
    """
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }


# ═══════════════════════════════════════════════════
# Page Factory фикстуры
# ═══════════════════════════════════════════════════

@pytest.fixture(scope='session')
def api_factory(base_url: str, api_headers: dict) -> APIFactory:
    """
    Page Factory для создания API объектов.

    Создает фабрику с базовым URL и заголовками.
    Все объекты кэшируются внутри фабрики.

    Args:
        base_url: URL API
        api_headers: Заголовки по умолчанию

    Yields:
        APIFactory: Фабрика Page Objects

    Example:
        def test_example(api_factory):
            operator_page = api_factory.get_operator_page()
            response = operator_page.get_all()
    """
    logger.info(f"Инициализация APIFactory для {base_url}")
    factory = APIFactory(base_url, default_headers=api_headers)

    yield factory

    # Cleanup: закрываем все сессии после тестов
    logger.info("Закрытие APIFactory")
    factory.close_all()


# ═══════════════════════════════════════════════════
# Page Object фикстуры
# ═══════════════════════════════════════════════════

@pytest.fixture(scope='session')
def operator_page(api_factory: APIFactory) -> OperatorPage:
    """
    Page Object для работы с операторами.

    Создается через фабрику и кэшируется.

    Args:
        api_factory: Фабрика Page Objects

    Returns:
        OperatorPage объект
    """
    return api_factory.get_operator_page()


@pytest.fixture(scope='session')
def country_page(api_factory: APIFactory) -> CountryPage:
    """
    Page Object для работы со странами.

    Args:
        api_factory: Фабрика Page Objects

    Returns:
        CountryPage объект
    """
    return api_factory.get_country_page()


# ═══════════════════════════════════════════════════
# Вспомогательные фикстуры
# ═══════════════════════════════════════════════════

@pytest.fixture(scope='session')
def country_helper(country_page: CountryPage) -> CountryHelper:
    """
    Вспомогательный объект для работы со странами.

    Args:
        country_page: Page Object стран

    Returns:
        CountryHelper объект
    """
    return CountryHelper(country_page)


@pytest.fixture(scope='session')
def country_ids(country_helper: CountryHelper) -> dict:
    """
    Словарь ID стран для использования в payload.

    Получает ID стран из API и кэширует на сессию.

    Args:
        country_helper: Вспомогательный объект

    Returns:
        Словарь с ключами rus_id, kor_id, mld_id
    """
    ids = country_helper.get_ids_dict()
    logger.info(f"Получены ID стран: {ids}")
    return ids


# ═══════════════════════════════════════════════════
# Payload фикстуры
# ═══════════════════════════════════════════════════

@pytest.fixture(scope='session')
def local_payload(country_ids: dict) -> dict:
    """
    Payload для создания локального оператора.

    Args:
        country_ids: ID стран

    Returns:
        Payload для локального оператора (Россия)
    """
    return local_operator_payload(country_ids)


@pytest.fixture(scope='session')
def praqe_payload(country_ids: dict) -> dict:
    """
    Payload для создания praqe оператора.

    Args:
        country_ids: ID стран

    Returns:
        Payload для praqe оператора (Молдова)
    """
    return praqe_operator_payload(country_ids)


@pytest.fixture(scope='session')
def all_payloads(local_payload: dict, praqe_payload: dict) -> list:
    """
    Список всех payload для параметризации.

    Args:
        local_payload: Локальный payload
        praqe_payload: Praqe payload

    Returns:
        Список payload'ов
    """
    return [local_payload, praqe_payload]
