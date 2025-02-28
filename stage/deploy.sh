#!/bin/bash

set -e

cd ~/opt/star-burger-1/stage

echo "Обновление кода из GitHub..."
git pull origin master

echo "Остановка старых контейнеров..."
docker compose down
docker system prune -a --volumes -f

echo "Сборка образов..."
docker compose build

echo "Запуск новых контейнеров..."
docker compose up -d

echo "Деплой завершен!"
