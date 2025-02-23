#!/bin/bash

DIRECTORY="/star-burger-1/stage"

cd "$DIRECTORY" || { echo "Директория не найдена: $DIRECTORY"; exit 1; }

echo "Остановка старых контейнеров..."
docker compose down

echo "Сборка образов..."
docker compose build

echo "Запуск новых контейнеров..."
docker compose up -d

echo "Деплой завершен!"
