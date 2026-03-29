# Инструкция по использованию API Test Framework

## Содержание

1. [Установка](#установка)
2. [Настройка окружения](#настройка-окружения)
3. [Запуск тестов](#запуск-тестов)
4. [Работа с Page Objects](#работа-с-page-objects)
5. [Создание новых тестов](#создание-новых-тестов)
6. [Работа с отчетами](#работа-с-отчетами)

---

## Установка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd autotest_api
```

### 2. Создание виртуального окружения

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Установка Allure (для просмотра отчетов)

**Windows (PowerShell):**
```powershell
scoop install allure
```

**macOS:**
```bash
brew install allure
```

**Linux:**
```bash
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

---

## Настройка окружения

### Создание файла .env

Скопируйте пример и отредактируйте:

```bash
cp .env.example .env
```

Откройте `.env` и укажите ваш API endpoint:

```env
CLIENT=https://your-api-endpoint.com/api/v1/
```

**Проверка настройки:**

```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('CLIENT:', os.getenv('CLIENT'))"
```

Должен вывести ваш URL.

---

## Запуск тестов

### Быстрый запуск через run.sh

```bash
# Все тесты (POST → GET)
./run.sh

# Только POST тесты (создание операторов)
./run.sh post

# Только GET тесты (получение данных)
./run.sh get

# Подробный вывод с дебагом
./run.sh debug
```

### Прямой запуск через pytest

```bash
# Все тесты с правильным порядком (POST перед GET)
pytest tests/ --order-dependencies -v

# Только POST тесты
pytest tests/post/ -v

# Только GET тесты
pytest tests/get/ -v

# Запуск конкретного теста
pytest tests/post/test_create_operators.py::TestCreateOperators::test_create_local_operator -v

# Запуск с генерацией Allure отчета
pytest tests/ --order-dependencies --alluredir=./allure-results -v
```

### Параметры pytest

| Параметр | Описание |
|----------|----------|
| `-v` | Подробный вывод |
| `-vv` | Очень подробный вывод |
| `--tb=short` | Короткий traceback |
| `--tb=long` | Длинный traceback |
| `-x` | Остановка после первого падения |
| `-k "test_create"` | Запуск тестов по имени |
| `-m "smoke"` | Запуск по маркеру |

---

## Работа с Page Objects

### Получение Page Object через Factory

```python
from api.factory import APIFactory

# Создание фабрики
factory = APIFactory("https://api.example.com/v1")

# Получение Page Objects
operator_page = factory.get_operator_page()
country_page = factory.get_country_page()

# Не забудьте закрыть сессии
factory.close_all()
```

### Использование в тестах (через фикстуры)

```python
def test_example(operator_page):
    # operator_page уже создан через Factory
    response = operator_page.get_all()
    assert response.status_code == 200
```

### Доступные методы OperatorPage

```python
# CREATE
response = operator_page.create({
    "name": "Test Operator",
    "country": {"countryId": 1, "countryName": "Russia"}
})

# READ
response = operator_page.get_all()                    # Все операторы
response = operator_page.get_by_id(123)              # Конкретный оператор
response = operator_page.get_by_country(1)             # По стране
response = operator_page.search("test")                # Поиск

# UPDATE
response = operator_page.update(123, {"name": "New"})    # Полное обновление
response = operator_page.partial_update(123, {...})    # Частичное обновление

# DELETE
response = operator_page.delete(123)

# Проверка существования
exists = operator_page.exists(123)  # True/False
```

### Доступные методы CountryPage

```python
# Получение всех стран
response = country_page.get_all()

# Получение по ID
response = country_page.get_by_id(1)

# Получение ID по коду (RUS, KOR, MDA)
country_id = country_page.get_id_by_code('RUS')  # Возвращает int или None

# Получение словаря всех ID
ids = country_page.get_all_ids()  # {'RUS': 1, 'KOR': 2, ...}

# Получение кодов всех стран
codes = country_page.get_country_codes()  # ['RUS', 'KOR', ...]

# Проверка существования
exists = country_page.country_exists('RUS')  # True/False
```

---

## Создание новых тестов

### 1. Создание POST теста

**Файл:** `tests/post/test_new_feature.py`

```python
import pytest
import allure
from utils.response_validators import ResponseValidator

@pytest.mark.order(1)  # POST тесты выполняются первыми
@allure.feature("New Feature")
@allure.story("Create Something")
def test_create_something(operator_page, local_payload):
    """Тест создания чего-то нового"""

    with allure.step("Отправка запроса"):
        response = operator_page.create(local_payload)

    with allure.step("Проверка ответа"):
        ResponseValidator.assert_status(response, 201)
        data = response.json()
        assert "id" in data
```

### 2. Создание GET теста

**Файл:** `tests/get/test_new_feature.py`

```python
import pytest
import allure

@pytest.mark.order(2)  # GET тесты выполняются после POST
@allure.feature("New Feature")
@allure.story("Get Something")
def test_get_something(operator_page):
    """Тест получения данных"""

    with allure.step("Получение списка"):
        response = operator_page.get_all()
        assert response.status_code == 200
```

### 3. Использование payload

```python
from payload.operator_payloads import create_operator_payload

# В тесте
custom_payload = create_operator_payload(
    name="Custom Operator",
    country_id=1,
    country_name="Russia",
    extra_field="value"
)

response = operator_page.create(custom_payload)
```

### 4. Использование валидаторов

```python
from utils.response_validators import (
    ResponseValidator,
    OperatorValidator
)

# Проверка статуса
ResponseValidator.assert_status(response, 200)
ResponseValidator.assert_status_in(response, [200, 201])

# Проверка полей
ResponseValidator.assert_has_field(data, "operatorId", int)
ResponseValidator.assert_has_fields(data, ["id", "name", "country"])

# Проверка для операторов
data = OperatorValidator.assert_created(response)  # Проверка 201
operators = OperatorValidator.assert_list_response(response)
```

---

## Работа с отчетами

### Генерация Allure отчета

```bash
# Запуск тестов с сохранением результатов
pytest tests/ --alluredir=./allure-results -v

# Просмотр отчета в браузере
allure serve ./allure-results

# Генерация статического отчета
allure generate ./allure-results -o ./allure-report --clean

# Открытие статического отчета
allure open ./allure-report
```

### Структура отчета Allure

```
allure-results/
├── *.json          # Результаты тестов
└── ...

allure-report/      # Генерируется allure generate
├── index.html      # Главная страница
└── ...
```

### Декораторы для отчетов

```python
import allure

@allure.feature("Operators API")      # Фича
@allure.story("Create Operations")  # История
@allure.title("Создание оператора") # Название теста
@allure.description("Подробное описание")
def test_create():
    with allure.step("Шаг 1: Подготовка"):
        # код
        pass

    with allure.step("Шаг 2: Выполнение"):
        # код
        pass

    with allure.step("Шаг 3: Проверка"):
        # код
        allure.attach(
            "Дополнительная информация",
            name="Debug info",
            attachment_type=allure.attachment_type.TEXT
        )
```

---

## Docker

### Быстрый запуск в Docker

```bash
# Сборка и запуск тестов
docker-compose up --build tests

# Запуск с Allure сервисом
docker-compose up --build allure

# Остановка
docker-compose down
```

### Просмотр отчета из Docker

```bash
# Запуск Allure сервиса
docker-compose up allure

# Откройте в браузере
http://localhost:4040
```

---

## Решение проблем

### Проблема: CLIENT не найден

**Решение:**
```bash
# Проверьте наличие .env файла
ls -la .env

# Проверьте содержимое
cat .env

# Должно быть:
# CLIENT=https://your-api.com/v1/
```

### Проблема: Тесты выполняются не по порядку

**Решение:**
```bash
# Обязательно используйте --order-dependencies
pytest tests/ --order-dependencies -v
```

### Проблема: ImportError

**Решение:**
```bash
# Убедитесь, что активировано виртуальное окружение
which python

# Установите зависимости
pip install -r requirements.txt

# Проверьте Python версию
python --version  # Должно быть 3.11+
```

### Проблема: Allure не найден

**Решение:**
```bash
# Проверка установки
allure --version

# Если не установлен, установите:
# macOS: brew install allure
# Linux: sudo apt-get install allure
# Windows: scoop install allure
```

---

## Примеры сценариев

### Сценарий 1: Создание и проверка оператора

```python
def test_create_and_verify(operator_page, local_payload):
    # Создаем
    create_response = operator_page.create(local_payload)
    data = create_response.json()
    operator_id = data['operatorId']

    # Получаем
    get_response = operator_page.get_by_id(operator_id)

    # Проверяем
    assert get_response.status_code == 200
    assert get_response.json()['operatorId'] == operator_id
```

### Сценарий 2: Поиск по стране

```python
def test_get_by_country(operator_page, country_page):
    # Получаем ID России
    rus_id = country_page.get_id_by_code('RUS')

    # Ищем операторов России
    response = operator_page.get_by_country(rus_id)

    # Проверяем
    assert response.status_code == 200
    operators = response.json()['items']
    assert len(operators) > 0
```

### Сценарий 3: Обновление оператора

```python
def test_update_operator(operator_page, local_payload):
    # Создаем
    created = operator_page.create(local_payload).json()
    operator_id = created['operatorId']

    # Обновляем
    updated = operator_page.update(operator_id, {
        "name": "Updated Name"
    }).json()

    # Проверяем
    assert updated['name'] == "Updated Name"
```

---

## Полезные команды

```bash
# Проверка синтаксиса всех файлов
python -m py_compile api/**/*.py tests/**/*.py

# Проверка установленных пакетов
pip list

# Обновление зависимостей
pip install --upgrade -r requirements.txt

# Очистка кэша pytest
pytest --cache-clear

# Запуск с профилированием времени
pytest tests/ --durations=10
```

---

## Контакты и поддержка

По вопросам и предложениям обращайтесь в Issues проекта.
