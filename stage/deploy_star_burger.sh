#!/bin/bash

set -e

cd ~/opt/star-burger-1/stage

echo "Обновление кода из GitHub..."
git pull origin master

echo "Остановка старых контейнеров..."
docker compose down

echo "Сборка образов и запуск новых контейнеров..."

docker compose up --build -d

echo "Деплой завершен!"
