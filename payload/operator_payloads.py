"""
Генераторы payload для операций с операторами.

Каждая функция создает структуру данных для конкретного сценария.
"""

from typing import Dict, Any, Optional


def local_operator_payload(
    country_ids: Optional[Dict[str, Any]] = None,
    **overrides
) -> Dict[str, Any]:
    """
    Создает payload для локального оператора (Россия).

    Args:
        country_ids: Словарь с ID стран (rus_id, kor_id, mld_id)
        **overrides: Поля для переопределения

    Returns:
        Payload для создания локального оператора
    """
    # Базовый payload
    payload = {
        "col1": "local_value1",
        "col2": "local_value2",
        "col3": {
            "col3col1": 5,
            "col3col2": "local_subvalue"
        },
        "country": {
            "countryId": country_ids.get('rus_id', 1) if country_ids else 1,
            "countryName": "Russia"
        }
    }

    # Применяем переопределения
    payload.update(overrides)
    return payload


def praqe_operator_payload(
    country_ids: Optional[Dict[str, Any]] = None,
    **overrides
) -> Dict[str, Any]:
    """
    Создает payload для praqe оператора (Молдова).

    Args:
        country_ids: Словарь с ID стран
        **overrides: Поля для переопределения

    Returns:
        Payload для создания praqe оператора
    """
    payload = {
        "col1": "praqe_value1",
        "col2": "praqe_value2",
        "col3": {
            "col3col1": 10,
            "col3col2": "praqe_subvalue"
        },
        "country": {
            "countryId": country_ids.get('mld_id', 3) if country_ids else 3,
            "countryName": "Moldova"
        }
    }

    payload.update(overrides)
    return payload


def create_operator_payload(
    name: str,
    country_id: int,
    country_name: str,
    **kwargs
) -> Dict[str, Any]:
    """
    Универсальная функция для создания payload оператора.

    Args:
        name: Название оператора
        country_id: ID страны
        country_name: Название страны
        **kwargs: Дополнительные поля

    Returns:
        Payload для создания оператора
    """
    payload = {
        "name": name,
        "country": {
            "countryId": country_id,
            "countryName": country_name
        }
    }

    # Добавляем стандартные поля, если не указаны
    if "col1" not in kwargs:
        kwargs["col1"] = "default_value1"
    if "col2" not in kwargs:
        kwargs["col2"] = "default_value2"

    payload.update(kwargs)
    return payload


def update_operator_payload(
    operator_id: int,
    **updates
) -> Dict[str, Any]:
    """
    Создает payload для обновления оператора.

    Args:
        operator_id: ID оператора
        **updates: Поля для обновления

    Returns:
        Payload для обновления оператора
    """
    payload = {
        "operatorId": operator_id
    }
    payload.update(updates)
    return payload


def invalid_operator_payload() -> Dict[str, Any]:
    """
    Создает невалидный payload для негативных тестов.

    Returns:
        Невалидный payload (отсутствует обязательное поле country)
    """
    return {
        "col1": "invalid",
        "col2": "invalid"
        # Нет country - должно вызвать ошибку валидации
    }


def minimal_operator_payload(country_id: int) -> Dict[str, Any]:
    """
    Создает минимальный валидный payload.

    Args:
        country_id: ID страны

    Returns:
        Минимальный payload
    """
    return {
        "country": {
            "countryId": country_id
        }
    }
