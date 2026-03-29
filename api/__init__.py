"""
API Page Objects and Factory module.

Provides Page Object pattern implementation for REST API testing.
"""

from .base_api import BaseAPI
from .factory import APIFactory

__all__ = ['BaseAPI', 'APIFactory']
