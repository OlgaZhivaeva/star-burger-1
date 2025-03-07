# Деплой проекта на сервер

[Ссылка на работающий сайт](http://80.249.146.244/)

Перейдите в директорию `stage`
```shell
$ cd ~/opt/star-burger-1/stage
```

Создайте файл `.env`  со следующими настройками:
```sh
SECRET_KEY=Секретный ключ щт вашего проекта Django
API_KEY_GEOKODER=Ваш API ключ для Яндекс-геокодера
DEBUG=True/False
ALLOWED_HOSTS=список хостов
ROLLBAR_TOKEN=Ваш токен от Rollbar, по умолчанию пустая строка
ROLLBAR_INVIRONMENT=Название окружения для Rollbar
POSTGRES_USER=Пользователь базы данных
POSTGRES_PASSWORD=Пароль
POSTGRES_DB=Имя базы данных
POSTGRES_DB_URL=postgres://nameuser:password@127.0.0.1:5432/namedb
```

Настройте конфиг Nginx
```
server {
    location / {
      include '/etc/nginx/proxy_params';
      proxy_pass http://127.0.0.1:8000/;
    }
    location /media/ {
        alias /home/<user>/opt/star-burger-1/backend/media/;
    }
    location /static/ {
        alias /home/<user>/opt/star-burger-1/backend/staticfiles/;
    }
    listen 80;
    server_name <server_IP>;
}
```

Для запуска проекта выполните команду
```shell
$ docker compose up
```

Для остановки контейнеров выполните команду
```shell
$ docker compose down
```

Запуск контейнеров после остановки
```shell
$ docker compose up --build
```

Создайте суперпользователя командой
```shell
$ docker exec -it django sh -c "python3 manage.py createsuperuser"
```

Для быстрого деплоя запустите скрипт `deploy_star_burger.sh`
```shell
$ ./deploy_star_burger.sh
```
