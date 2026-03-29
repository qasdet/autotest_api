"""
Page Objects для API эндпоинтов.

Каждый класс представляет собой Page Object для конкретного ресурса API,
инкапсулируя URL, параметры и логику работы с эндпоинтом.
"""

from .operator_page import OperatorPage
from .country_page import CountryPage

__all__ = ['OperatorPage', 'CountryPage']
