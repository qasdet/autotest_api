# API Test Framework с Page Object и Page Factory

Фреймворк для автоматизации API тестирования с использованием паттернов **Page Object** и **Page Factory**.

---

## 🏗️ Архитектура

### Паттерны

**Page Object** — инкапсулирует работу с API ресурсами:
```python
class OperatorPage:
    def create(self, data):      # POST /operators
    def get_all(self):           # GET /operators
    def get_by_id(self, id):     # GET /operators/{id}
    def update(self, id, data):  # PUT /operators/{id}
    def delete(self, id):        # DELETE /operators/{id}
```

**Page Factory** — централизованное создание и кэширование Page Objects:
```python
factory = APIFactory(base_url)
operator_page = factory.get_operator_page()  # Создается один раз
country_page = factory.get_country_page()
```

---

## 📁 Структура проекта

```
autotest_api/
│
├── api/                          # Page Objects и Factory
│   ├── base_api.py              # Базовый HTTP-класс
│   ├── factory.py               # Page Factory
│   └── page_objects/
│       ├── base_page.py         # Базовый Page Object
│       ├── operator_page.py     # Page Object для /operators
│       └── country_page.py      # Page Object для /countries
│
├── payload/                      # Генераторы данных
│   └── operator_payloads.py     # Payload для операторов
│
├── tests/                        # Тесты
│   ├── conftest.py              # Фикстуры с Page Factory
│   ├── post/                    # POST тесты (order=1)
│   │   └── test_create_operators.py
│   └── get/                     # GET тесты (order=2)
│       ├── test_get_operators.py
│       └── test_get_countries.py
│
├── utils/                        # Вспомогательные классы
│   ├── response_validators.py   # Валидаторы ответов
│   └── country_helper.py        # Хелпер для стран
│
├── pytest.ini                   # Конфигурация pytest
├── requirements.txt             # Зависимости
├── Dockerfile                   # Docker образ
└── README.md                    # Документация
```

---

## 🚀 Быстрый старт

### Установка

```bash
# Клонирование
git clone <repository>
cd autotest_api

# Создание окружения
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt

# Настройка окружения
cp .env.example .env
# Отредактируйте .env
```

### Запуск тестов

```bash
# Все тесты (POST → GET)
./run.sh

# Или напрямую через pytest
pytest tests/ --order-dependencies --alluredir=./allure-results -v

# Только POST
./run.sh post
pytest tests/post/ -v

# Только GET
./run.sh get
pytest tests/get/ -v

# С отчетом Allure
allure serve ./allure-results
```

---

## 📖 Page Objects

### OperatorPage

```python
from api.factory import APIFactory

factory = APIFactory("https://api.example.com/v1")
operator = factory.get_operator_page()

# CREATE
response = operator.create({"name": "Test", "countryId": 1})

# READ
response = operator.get_all()                    # GET /operators
response = operator.get_by_id(123)              # GET /operators/123
response = operator.get_by_country(1)           # GET /operators?countryId=1
response = operator.search("test")                # GET /operators?search=test

# UPDATE
response = operator.update(123, {"name": "New"})  # PUT /operators/123
response = operator.partial_update(123, {...}) # PATCH /operators/123

# DELETE
response = operator.delete(123)                  # DELETE /operators/123
```

### CountryPage

```python
country = factory.get_country_page()

# Получение всех стран
response = country.get_all()

# Получение по коду
country_id = country.get_id_by_code('RUS')  # Возвращает ID

# Получение словаря ID
ids = country.get_all_ids()  # {'RUS': 1, 'KOR': 2, ...}
```

---

## 🔧 Фикстуры

```python
# tests/conftest.py

@pytest.fixture(scope='session')
def api_factory(base_url):
    """Page Factory для создания API объектов"""
    factory = APIFactory(base_url)
    yield factory
    factory.close_all()  # Cleanup

@pytest.fixture(scope='session')
def operator_page(api_factory):
    """Page Object для операторов"""
    return api_factory.get_operator_page()

@pytest.fixture(scope='session')
def country_page(api_factory):
    """Page Object для стран"""
    return api_factory.get_country_page()

@pytest.fixture(scope='session')
def local_payload(country_ids):
    """Payload для локального оператора"""
    return local_operator_payload(country_ids)
```

---

## 🧪 Примеры тестов

### POST тест

```python
@pytest.mark.order(1)  # Выполняется первым
@allure.feature("Create Operators")
def test_create_local_operator(operator_page, local_payload):
    """Тест создания локального оператора"""
    response = operator_page.create(local_payload)
    data = OperatorValidator.assert_created(response)
    assert data['operatorId'] is not None
```

### GET тест

```python
@pytest.mark.order(2)  # Выполняется после POST
@allure.feature("Get Operators")
def test_get_all_operators(operator_page):
    """Тест получения списка операторов"""
    response = operator_page.get_all()
    operators = OperatorValidator.assert_list_response(response)
    assert len(operators) > 0
```

---

## 🐳 Docker

```bash
# Сборка и запуск
./run.sh docker

# Или напрямую
docker-compose up --build tests

# С Allure сервисом
docker-compose up --build allure
# Откройте http://localhost:4040
```

---

## 📝 Payload генераторы

```python
from payload.operator_payloads import (
    local_operator_payload,
    praqe_operator_payload,
    create_operator_payload
)

# Создание payload
local = local_operator_payload(country_ids)
praqe = praqe_operator_payload(country_ids)

# Универсальный генератор
custom = create_operator_payload(
    name="Custom Operator",
    country_id=1,
    country_name="Russia",
    extra_field="value"
)
```

---

## ✅ Валидаторы

```python
from utils.response_validators import (
    ResponseValidator,
    OperatorValidator,
    CountryValidator
)

# Общие проверки
ResponseValidator.assert_status(response, 200)
ResponseValidator.assert_has_field(data, 'operatorId', int)

# Специфичные для операторов
OperatorValidator.assert_created(response)      # Проверка 201
OperatorValidator.assert_list_response(response)  # Проверка списка

# Специфичные для стран
CountryValidator.assert_has_country_fields(data)
```

---

## 🔌 Расширение

### Добавление нового Page Object

```python
# 1. Создайте класс в api/page_objects/
class UserPage(BasePage):
    RESOURCE = "users"

    def create(self, data):
        return self.post(self._resource_url(), json=data)

# 2. Добавьте в Factory
class APIFactory:
    def get_user_page(self):
        return self._get_or_create('user', UserPage)

# 3. Добавьте фикстуру
@pytest.fixture(scope='session')
def user_page(api_factory):
    return api_factory.get_user_page()

# 4. Используйте в тесте
def test_create_user(user_page):
    response = user_page.create({"name": "Test"})
    assert response.status_code == 201
```

---

## 📊 Allure отчеты

```bash
# Запуск с генерацией отчета
pytest tests/ --alluredir=./allure-results

# Просмотр
allure serve ./allure-results

# Статический отчет
allure generate ./allure-results -o ./allure-report --clean
```

---

## 📄 Лицензия

MIT
