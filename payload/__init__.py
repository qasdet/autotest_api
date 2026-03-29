"""
Генераторы payload для API запросов.

Содержит функции для создания тестовых данных различных типов.
"""

from .operator_payloads import (
    local_operator_payload,
    praqe_operator_payload,
    create_operator_payload,
    update_operator_payload
)

__all__ = [
    'local_operator_payload',
    'praqe_operator_payload',
    'create_operator_payload',
    'update_operator_payload'
]
