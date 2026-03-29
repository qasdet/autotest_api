FROM python:3.11-slim

# Метаданные образа
LABEL maintainer="API Test Framework"
LABEL description="API Test Framework с Page Object и Page Factory"

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Создание директории для результатов Allure
RUN mkdir -p /app/allure-results

# Переменная окружения для Allure
ENV ALLURE_RESULTS_DIRECTORY=/app/allure-results

# Команда по умолчанию
CMD ["pytest", "tests/", "--order-dependencies", "--alluredir=/app/allure-results", "-v"]
