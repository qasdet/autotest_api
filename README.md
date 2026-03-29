# Документация API Test Framework

## 📋 Содержание

1. [Обзор проекта](#обзор-проекта)
2. [Архитектура](#архитектура)
3. [Структура проекта](#структура-проекта)
4. [Установка и настройка](#установка-и-настройка)
5. [Запуск тестов](#запуск-тестов)
6. [Описание модулей](#описание-модулей)
7. [Интеграция с Allure TestOps](#интеграция-с-allure-testops)
8. [Docker](#docker)
9. [CI/CD](#cicd)
10. [Расширение фреймворка](#расширение-фреймворка)

---

## Обзор проекта

API Test Framework — это Python-фреймворк для автоматизации тестирования REST API с использованием:
- **pytest** — запуск тестов
- **requests** — HTTP-запросы
- **pytest-order** — управление порядком выполнения тестов
- **Allure** — генерация отчетов
- **Docker** — контейнеризация
- **GitLab CI/GitHub Actions** — непрерывная интеграция

### Особенности

✅ **Упорядоченное выполнение**: POST-тесты всегда выполняются перед GET-тестами
✅ **Allure интеграция**: Подробные отчеты с шагами, вложениями и метаданными
✅ **Docker-контейнеризация**: Запуск в изолированной среде
✅ **CI/CD готовность**: Готовые конфигурации для GitLab и GitHub
✅ **Модульная архитектура**: Легко расширять и поддерживать

---

## Архитектура

### Паттерн Page Object Model (для API)

Фреймворк использует адаптацию паттерна Page Object для API:

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   BaseAPI       │────▶│  Endpoints       │────�│   API Client    │
│   (базовый      │     │   (URL константы)│     │   Classes       │
│   HTTP-класс)   │     │                  │     │   (методы API)  │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Tests         │◀────│  Fixtures        │◀────│   Payload       │
│   (тест-кейсы)  │     │   (подготовка    │     │   (данные для   │
│                 │     │    данных)       │     │    запросов)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

### Порядок выполнения тестов

```
Session Start
    │
    ▼
┌─────────────────────────────────────────┐
│  FIXTURES (session scope)               │
│  • get_base_url()                       │
│  • base_api()                          │
│  • get_country() → country_ids()       │
│  • oper_local_payload()                │
│  • oper_praqe_payload()                │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  ORDER 1: POST ТЕСТЫ                   │
│  assertions/01_create/                 │
│  • test_post_broker[oper_local_payload]│
│  • test_post_broker[oper_praqe_payload]│
└─────────────────────────────────────────┘
    │
    ▼ (зависимость через --order-dependencies)
┌─────────────────────────────────────────┐
│  ORDER 2: GET ТЕСТЫ                    │
│  assertions/02_get/                    │
│  • test_get_operators()                │
└─────────────────────────────────────────┘
```

---

## Структура проекта

```
autotest_api/
│
├── api_frame/                    # HTTP-клиенты и API-обертки
│   ├── __init__.py
│   ├── base_api.py              # Базовый класс для HTTP-запросов
│   ├── endpoints.py             # URL-константы API
│   ├── create_operator.py       # Класс для POST /operators
│   ├── get_operators.py         # Класс для GET /operators
│   └── get_countries.py         # Класс для GET /countries (получение countryId)
│
├── assertions/                   # Тесты и валидация
│   ├── __init__.py
│   ├── conftest.py              # Фикстуры pytest (session scope)
│   ├── assertions.py            # Функции контрактной проверки (заглушка)
│   ├── 01_create/               # POST-тесты (выполняются первыми)
│   │   ├── __init__.py
│   │   └── test_post_operator.py
│   └── 02_get/                  # GET-тесты (выполняются после POST)
│       ├── __init__.py
│       └── test_get_operators.py
│
├── dict_payload/                 # Тестовые данные (payload)
│   ├── __init__.py
│   ├── conftest.py
│   └── payload_create_oper.py   # JSON-структуры для создания операторов
│
├── tools/                        # Вспомогательные утилиты
│   ├── __init__.py
│   ├── conftest.py
│   └── get_country_id.py        # Получение ID стран из API
│
├── .github/workflows/            # GitHub Actions CI/CD
│   └── test.yml
│
├── .gitlab-ci.yml                # GitLab CI/CD (полная конфигурация)
├── .gitlab-ci-LOCAL.yml          # GitLab CI/CD (шаблон для ручной настройки)
│
├── Dockerfile                    # Образ Docker для тестов
├── docker-compose.yml            # Docker Compose конфигурация
├── pytest.ini                   # Настройки pytest
├── requirements.txt             # Python-зависимости
├── run.sh                       # Скрипт запуска тестов
├── .env.example                 # Пример переменных окружения
└── README.md                    # Эта документация
```

---

## Установка и настройка

### 1. Требования

- Python 3.11+
- pip
- Docker (опционально)
- Allure Commandline (для просмотра отчетов)

### 2. Клонирование и установка

```bash
# Клонировать репозиторий
git clone <repository-url>
cd autotest_api

# Создать виртуальное окружение (рекомендуется)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установить зависимости
pip install -r requirements.txt
```

### 3. Настройка окружения

```bash
# Скопировать пример конфигурации
cp .env.example .env

# Отредактировать .env файл
CLIENT=https://your-api-endpoint.com/api/v1/
```

**Переменные окружения:**

| Переменная | Описание | Обязательная |
|------------|----------|--------------|
| `CLIENT` | Базовый URL API | Да |
| `ALLURE_TOKEN` | API токен Allure TestOps | Нет |
| `ALLURE_PROJECT_ID` | ID проекта в Allure TestOps | Нет |
| `ALLURE_TESTOPS_ENDPOINT` | URL Allure TestOps | Нет |

---

## Запуск тестов

### Локальный запуск

```bash
# Все тесты с правильным порядком (POST → GET)
pytest --order-dependencies --alluredir=./allure-results -v

# Только POST тесты
pytest assertions/01_create/ -v

# Только GET тесты
pytest assertions/02_get/ -v

# С генерацией Allure отчета
pytest --order-dependencies --alluredir=./allure-results -v
allure serve ./allure-results
```

### Через run.sh

```bash
# Сделать скрипт исполняемым
chmod +x run.sh

# Запустить
./run.sh
```

### В Docker

```bash
# Собрать и запустить
docker-compose up --build tests

# С запуском Allure сервиса
docker-compose up --build

# Открыть отчет: http://localhost:4040
```

---

## Описание модулей

### api_frame/

#### base_api.py

Базовый класс для HTTP-запросов с использованием `requests.Session`.

**Методы:**
- `_send_request(method, endpoint, **kwargs)` — базовый метод отправки
- `get_request(endpoint, **kwargs)` — GET-запрос
- `post_request(endpoint, **kwargs)` — POST-запрос
- `put_request(endpoint, **kwargs)` — PUT-запрос

**Особенности:**
- Использует Session для переиспользования соединений
- Автоматически поднимает исключения при HTTP-ошибках
- Формирует полный URL: `{base_url}{endpoint}`

#### endpoints.py

Константы URL-эндпоинтов API.

```python
POST_OPERATOR = 'test'      # POST /test
GET_OPERATOR = 'test'       # GET /test
GET_COUNTRY = 'test'        # GET /test (countries)
```

> **Примечание:** В текущей конфигурации все эндпоинты указывают на 'test'. Измените на реальные пути API.

#### create_operator.py

```python
from api_frame.create_operator import CreateOperatorAPI

create_api = CreateOperatorAPI(base_url)
response = create_api.create_operator(payload)
```

#### get_operators.py

```python
from api_frame.get_operators import GetOperatorsAPI

get_api = GetOperatorsAPI(base_url)
response = get_api.get_operators()  # Возвращает Response object
```

#### get_countries.py

```python
from api_frame.get_countries import GetCountries

countries_api = GetCountries(base_url)
country_id = countries_api.get_country_id('RUS')  # Получить ID по коду страны
```

### assertions/

#### conftest.py

Фикстуры с scope='session' — выполняются один раз за сессию тестирования.

**Фикстуры:**
- `get_base_url()` — URL из переменной окружения `CLIENT`
- `create_oper(get_base_url)` — экземпляр CreateOperatorAPI
- `get_country(get_base_url)` — экземпляр GetCountries
- `country_ids(get_country)` — словарь с ID стран (rus_id, kor_id, mld_id)
- `oper_local_payload(country_ids)` — payload для локального оператора
- `oper_praqe_payload(country_ids)` — payload для praqe оператора
- `get_operators(get_base_url)` — экземпляр GetOperatorsAPI

#### test_post_operator.py

POST-тесты с маркером `@pytest.mark.order(1)`.

```python
@pytest.mark.order(1)  # Выполняется первым
@pytest.mark.parametrize("all_operator", [
    "oper_local_payload",
    "oper_praqe_payload"
])
def test_post_broker(create_oper, all_operator, ...):
    # Создает двух операторов через параметризацию
```

**Allure декораторы:**
- `@allure.feature("Operators API")` — фича
- `@allure.story("Create Operators")` — пользовательская история
- `@allure.title("Create operator with {all_operator}")` — название теста

#### test_get_operators.py

GET-тест с маркером `@pytest.mark.order(2)`.

```python
@pytest.mark.order(2)  # Выполняется после POST тестов
def test_get_operators(get_operators):
    # Получает список операторов
```

### dict_payload/

#### payload_create_oper.py

Функции-генераторы payload для создания операторов.

```python
def localoperator(country_ids=None):
    """Payload для локального оператора (Россия)"""
    return {
        "col1": "value1",
        "col2": "value2",
        "col3": { ... },
        "country": {
            "countryId": country_ids['rus_id'],
            "countryName": "Russia"
        }
    }

def oper_praqe(country_ids=None):
    """Payload для praqe оператора (Молдова)"""
    return { ... }
```

### tools/

#### get_country_id.py

```python
def get_country_ids(get_country):
    """Получает ID стран из API /countries"""
    return {
        'rus_id': ...,  # Россия
        'kor_id': ...,  # Корея
        'mld_id': ...   # Молдова
    }
```

---

## Интеграция с Allure TestOps

### Локальный просмотр отчетов

```bash
# Установить Allure CLI
# macOS:
brew install allure

# Linux:
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure

# Windows:
scoop install allure
```

```bash
# Сгенерировать и открыть отчет
pytest --alluredir=./allure-results
allure serve ./allure-results

# Или сгенерировать статический отчет
allure generate ./allure-results -o ./allure-report --clean
allure open ./allure-report
```

### Ручная загрузка в Allure TestOps

```bash
# 1. Упаковать результаты
cd allure-results && zip -r ../allure-results.zip .

# 2. Загрузить через curl
curl -X POST "${ALLURE_ENDPOINT}/api/rs/launch/import" \
  -H "Authorization: Api-Token ${ALLURE_TOKEN}" \
  -F "projectId=${ALLURE_PROJECT_ID}" \
  -F "results=@allure-results.zip"
```

### Docker с Allure Service

```bash
docker-compose up allure
# Открыть http://localhost:4040
```

Переменные Allure Docker Service:
- `CHECK_RESULTS_EVERY_SECONDS=5` — частота проверки новых результатов
- `KEEP_HISTORY=1` — сохранять историю
- `KEEP_HISTORY_LATEST=20` — количество сохраняемых отчетов

---

## Docker

### Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
# Установка системных зависимостей
RUN apt-get update && apt-get install -y gcc
# Копирование и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Копирование проекта
COPY . .
# Команда по умолчанию
CMD ["pytest", "--order-dependencies", "--alluredir=/app/allure-results"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  tests:
    build: .
    container_name: autotest_api
    volumes:
      - ./allure-results:/app/allure-results
    environment:
      - CLIENT=${CLIENT}
    command: pytest --order-dependencies --alluredir=/app/allure-results -v

  allure:
    image: frankescobar/allure-docker-service:latest
    ports:
      - "4040:4040"  # Веб-интерфейс
    volumes:
      - ./allure-results:/app/allure-results
```

### Команды Docker

```bash
# Сборка образа
docker build -t autotest-api .

# Запуск тестов
docker run --rm \
  -e CLIENT=https://api.example.com/v1/ \
  -v $(pwd)/allure-results:/app/allure-results \
  autotest-api

# Полный запуск с Allure
docker-compose up --build
```

---

## CI/CD

### GitLab CI

#### Основные задачи:

1. **run-tests** — запуск тестов с сохранением артефактов
2. **generate-allure-report** — генерация HTML отчета
3. **publish-to-testops** — публикация в Allure TestOps
4. **pages** — публикация на GitLab Pages

#### Переменные GitLab CI/CD:

Настройки → CI/CD → Переменные:

| Переменная | Защищенная | Маскированная |
|------------|-----------|---------------|
| `CLIENT_URL` | Да | Нет |
| `ALLURE_TOKEN` | Да | Да |
| `ALLURE_PROJECT_ID` | Да | Нет |
| `ALLURE_TESTOPS_ENDPOINT` | Да | Нет |

#### Использование шаблона:

```bash
# Для быстрого старта:
cp .gitlab-ci-LOCAL.yml .gitlab-ci.yml
# Заполните переменные в GitLab UI
```

### GitHub Actions

#### Workflow файл: `.github/workflows/test.yml`

**Триггеры:**
- Push в `main` или `develop`
- Pull Request в `main`
- Расписание: каждый день в 2:00

**Jobs:**
1. **test** — установка Python, зависимостей, запуск тестов
2. **upload-testops** — загрузка результатов в Allure TestOps (опционально)

#### Секреты GitHub:

Settings → Secrets and variables → Actions:

- `CLIENT_URL`
- `ALLURE_TOKEN`
- `ALLURE_PROJECT_ID`
- `ALLURE_ENDPOINT`

---

## Расширение фреймворка

### Добавление нового endpoint

1. **Добавить константу** в `api_frame/endpoints.py`:
```python
DELETE_OPERATOR = 'operators/{operator_id}'
```

2. **Создать класс** в `api_frame/delete_operator.py`:
```python
from api_frame.base_api import BaseAPI
from api_frame.endpoints import DELETE_OPERATOR

class DeleteOperatorAPI(BaseAPI):
    endpoint = DELETE_OPERATOR

    def delete_operator(self, operator_id):
        endpoint = self.endpoint.format(operator_id=operator_id)
        return self.delete_request(endpoint=endpoint)
```

3. **Добавить метод в BaseAPI** (если нужен DELETE):
```python
def delete_request(self, endpoint, **kwargs):
    return self._send_request('DELETE', endpoint, **kwargs)
```

4. **Создать фикстуру** в `assertions/conftest.py`:
```python
@pytest.fixture(scope='session')
def delete_operator(get_base_url):
    return DeleteOperatorAPI(get_base_url)
```

5. **Создать тест** в новом пакете `assertions/03_delete/`:
```python
import pytest
import allure

@pytest.mark.order(3)  # После POST и GET
def test_delete_operator(delete_operator):
    with allure.step("Delete operator"):
        response = delete_operator.delete_operator(123)
    assert response.status_code == 204
```

### Добавление нового payload

1. **Добавить функцию** в `dict_payload/payload_create_oper.py`:
```python
def new_operator(country_ids=None):
    return {
        "col1": "value",
        "country": {
            "countryId": country_ids.get('new_id', country_ids['rus_id']),
            "countryName": "New Country"
        }
    }
```

2. **Добавить фикстуру** в `assertions/conftest.py`:
```python
@pytest.fixture(scope='session')
def oper_new_payload(country_ids):
    return new_operator(country_ids)
```

3. **Использовать в тесте**:
```python
@pytest.mark.parametrize("all_operator", [
    "oper_local_payload",
    "oper_praqe_payload",
    "oper_new_payload"  # Новый payload
])
```

### Добавление ассертов

1. **Реализовать функцию** в `assertions/assertions.py`:
```python
def assert_operator_created(response_data, expected_payload):
    """Проверяет, что оператор создан с корректными данными"""
    assert 'operatorId' in response_data, "Ответ должен содержать operatorId"
    assert response_data['country']['countryName'] == expected_payload['country']['countryName']
```

2. **Использовать в тесте**:
```python
data = response.json()
assert_operator_created(data, oper_data)
```

---

## Troubleshooting

### Проблема: ImportError при запуске

```bash
# Убедитесь, что установлены все зависимости
pip install -r requirements.txt

# Проверьте Python версию
python --version  # Должно быть 3.11+
```

### Проблема: Тесты выполняются не по порядку

```bash
# Обязательно используйте флаг --order-dependencies
pytest --order-dependencies ...

# Проверьте установку плагина
pip list | grep pytest-order
```

### Проблема: Allure не генерирует отчет

```bash
# Проверьте установку allure-pytest
pip list | grep allure

# Убедитесь, что директория для результатов существует
mkdir -p ./allure-results
```

### Проблема: Docker не видит .env файл

```bash
# Docker не подхватывает .env автоматически
# Используйте явное указание переменных
docker run -e CLIENT=$CLIENT ...

# Или в docker-compose.yml укажите env_file:
env_file:
  - .env
```

---

## Лицензия

MIT License

---

## Контакты

По вопросам и предложениям обращайтесь в Issues репозитория.
