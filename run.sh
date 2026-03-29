#!/bin/bash

# ════════════════════════════════════════════════════════════
# Скрипт для запуска API тестов
# Использует Page Factory паттерн через pytest
# ════════════════════════════════════════════════════════════

set -e

# Цвета для вывода
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     API Test Framework - Page Factory          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠ Файл .env не найден. Создайте его из .env.example${NC}"
    echo ""
fi

# Функция для генерации отчета
generate_report() {
    echo -e "${BLUE}═════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✓ Тесты завершены!${NC}"
    echo ""
    echo "Для просмотра отчета Allure:"
    echo -e "${YELLOW}  allure serve ./allure-results${NC}"
    echo ""
    echo "Или сгенерируйте статический отчет:"
    echo -e "${YELLOW}  allure generate ./allure-results -o ./allure-report${NC}"
    echo -e "${BLUE}═════════════════════════════════════════════════${NC}"
}

# Режим запуска
MODE=${1:-"all"}

case $MODE in
    "all")
        echo -e "${BLUE}▶ Запуск всех тестов с порядком POST → GET${NC}"
        echo ""
        pytest tests/ --order-dependencies -v
        generate_report
        ;;
    "post")
        echo -e "${BLUE}▶ Запуск только POST тестов${NC}"
        echo ""
        pytest tests/post/ -v
        ;;
    "get")
        echo -e "${BLUE}▶ Запуск только GET тестов${NC}"
        echo ""
        pytest tests/get/ -v
        ;;
    "smoke")
        echo -e "${BLUE}▶ Запуск smoke тестов${NC}"
        echo ""
        pytest tests/ -m smoke -v
        ;;
    "debug")
        echo -e "${BLUE}▶ Запуск с подробным выводом${NC}"
        echo ""
        pytest tests/ --order-dependencies -vv --tb=long
        ;;
    *)
        echo "Использование: ./run.sh [all|post|get|smoke|debug]"
        echo ""
        echo "  all    - все тесты (POST → GET)"
        echo "  post   - только POST тесты"
        echo "  get    - только GET тесты"
        echo "  smoke  - smoke тесты"
        echo "  debug  - подробный вывод"
        exit 1
        ;;
esac
