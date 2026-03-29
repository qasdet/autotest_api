# Docker Setup Guide

## Quick Start
```bash
# Build and run tests
docker-compose up --build tests

# Run with Allure report service
docker-compose up --build
```

## Manual Docker Commands
```bash
# Build image
docker build -t autotest-api .

# Run tests
docker run --rm -v $(pwd)/allure-results:/app/allure-results autotest-api

# Run with environment variables
docker run --rm \
  -e CLIENT=https://api.example.com/api/v1/ \
  -v $(pwd)/allure-results:/app/allure-results \
  autotest-api
```

## Viewing Reports
```bash
# After running tests, start Allure service
docker-compose up allure

# Open browser at http://localhost:4040
```
