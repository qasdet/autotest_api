#!/bin/bash

# Запуск тестов с правильным порядком: сначала POST, потом GET
# Используется плагин pytest-order с флагом --order-dependencies

echo "=========================================="
echo "Запуск API тестов в порядке POST -> GET"
echo "=========================================="

pytest assertions/ --order-dependencies --alluredir=./allure-results -v

echo "=========================================="
echo "Тесты завершены. Для просмотра отчета:"
echo "allure serve ./allure-results"
echo "=========================================="