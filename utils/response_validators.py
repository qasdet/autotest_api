"""
Валидаторы для проверки HTTP-ответов.
"""

from typing import Dict, Any, List, Optional, Callable
import requests


class ResponseValidator:
    """
    Класс для валидации HTTP-ответов.

    Предоставляет методы для проверки статусов, структуры данных
    и бизнес-логики ответов API.
    """

    @staticmethod
    def assert_status(
        response: requests.Response,
        expected_status: int
    ) -> None:
        """
        Проверяет статус ответа.

        Args:
            response: HTTP-ответ
            expected_status: Ожидаемый статус код

        Raises:
            AssertionError: Если статус не совпадает
        """
        assert response.status_code == expected_status, (
            f"Ожидался статус {expected_status}, "
            f"получен {response.status_code}. "
            f"Тело ответа: {response.text[:500]}"
        )

    @staticmethod
    def assert_status_in(
        response: requests.Response,
        expected_statuses: List[int]
    ) -> None:
        """
        Проверяет, что статус в списке допустимых.

        Args:
            response: HTTP-ответ
            expected_statuses: Список допустимых статусов
        """
        assert response.status_code in expected_statuses, (
            f"Ожидался один из статусов {expected_statuses}, "
            f"получен {response.status_code}"
        )

    @staticmethod
    def assert_has_field(
        data: Dict[str, Any],
        field: str,
        field_type: Optional[type] = None
    ) -> Any:
        """
        Проверяет наличие поля в данных.

        Args:
            data: Данные для проверки
            field: Имя поля
            field_type: Ожидаемый тип поля (опционально)

        Returns:
            Значение поля

        Raises:
            AssertionError: Если поле отсутствует
        """
        assert field in data, f"Ответ должен содержать поле '{field}'"
        value = data[field]

        if field_type is not None:
            assert isinstance(value, field_type), (
                f"Поле '{field}' должно быть типа {field_type}, "
                f"получен {type(value)}"
            )

        return value

    @staticmethod
    def assert_has_fields(
        data: Dict[str, Any],
        fields: List[str]
    ) -> None:
        """
        Проверяет наличие нескольких полей.

        Args:
            data: Данные для проверки
            fields: Список обязательных полей
        """
        for field in fields:
            assert field in data, f"Ответ должен содержать поле '{field}'"

    @staticmethod
    def assert_list_not_empty(data: List[Any]) -> None:
        """
        Проверяет, что список не пустой.

        Args:
            data: Список для проверки
        """
        assert isinstance(data, list), "Данные должны быть списком"
        assert len(data) > 0, "Список не должен быть пустым"

    @staticmethod
    def assert_json_structure(
        data: Dict[str, Any],
        expected_structure: Dict[str, Any]
    ) -> None:
        """
        Рекурсивно проверяет структуру JSON.

        Args:
            data: Данные для проверки
            expected_structure: Ожидаемая структура с типами
        """
        for key, expected_type in expected_structure.items():
            assert key in data, f"Отсутствует ключ '{key}'"

            if isinstance(expected_type, dict):
                # Рекурсивная проверка вложенной структуры
                assert isinstance(data[key], dict), (
                    f"Поле '{key}' должно быть объектом"
                )
                ResponseValidator.assert_json_structure(
                    data[key],
                    expected_type
                )
            elif isinstance(expected_type, list) and expected_type:
                # Проверка массива
                assert isinstance(data[key], list), (
                    f"Поле '{key}' должно быть массивом"
                )
                if data[key]:
                    ResponseValidator.assert_json_structure(
                        data[key][0],
                        expected_type[0]
                    )
            elif expected_type is not None:
                # Проверка типа
                assert isinstance(data[key], expected_type), (
                    f"Поле '{key}' должно быть типа {expected_type}"
                )


class OperatorValidator(ResponseValidator):
    """
    Валидатор специфичный для операторов.
    """

    @staticmethod
    def assert_created(response: requests.Response) -> Dict[str, Any]:
        """
        Проверяет успешное создание оператора.

        Args:
            response: Ответ от POST /operators

        Returns:
            Данные созданного оператора
        """
        ResponseValidator.assert_status_in(response, [200, 201])
        data = response.json()

        ResponseValidator.assert_has_fields(
            data,
            ['operatorId', 'country']
        )

        return data

    @staticmethod
    def assert_list_response(response: requests.Response) -> List[Dict[str, Any]]:
        """
        Проверяет ответ со списком операторов.

        Args:
            response: Ответ от GET /operators

        Returns:
            Список операторов
        """
        ResponseValidator.assert_status(response, 200)
        data = response.json()

        # Поддержка разных структур ответа
        items = data.get('items', []) or data.get('operators', []) or data

        if not isinstance(items, list):
            items = [items]

        return items


class CountryValidator(ResponseValidator):
    """
    Валидатор специфичный для стран.
    """

    @staticmethod
    def assert_has_country_fields(data: Dict[str, Any]) -> None:
        """
        Проверяет наличие обязательных полей страны.

        Args:
            data: Данные страны
        """
        ResponseValidator.assert_has_fields(
            data,
            ['countryId', 'countryCode']
        )
