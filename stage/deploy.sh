#!/bin/bash

set -e

cd ~/opt/star-burger-1/stage

echo "Остановка старых контейнеров..."
docker compose down

echo "Сборка образов..."
docker compose build

echo "Запуск новых контейнеров..."
docker compose up -d

echo "Деплой завершен!"
