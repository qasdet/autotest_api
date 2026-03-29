FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements и установка Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование файлов проекта
COPY . .

# Создание директории для результатов Allure
RUN mkdir -p /app/allure-results

# Переменная окружения для результатов Allure
ENV ALLURE_RESULTS_DIRECTORY=/app/allure-results

# Команда по умолчанию для запуска тестов
CMD ["pytest", "--order-dependencies", "--alluredir=/app/allure-results"]
