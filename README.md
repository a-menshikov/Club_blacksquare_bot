# Бот для СКИТ Чёрный Квадрат

## Описание

Бот для клуба интеллектуальных игр Чёрный квадрат (г.Северодвинск) позволяющий следить за календарём событий клуба.
Поддерживает CRUD для событий, умеет уведомлять о предстоящих событиях
ссылка <https://t.me/club_blacksquare_bot>

## Технологии

- python==3.10
- aiogram==2.25.1
- SQLAlchemy==2.0.7
- aioschedule==0.5.2

## Формат файла .env

```python
# токен телеграм бота, формат string
T_TOKEN = ''

# телеграм_id админа бота, которому доступны CRUD операции над событиями, формат string
# если админов несколько - указывать id последовательно в строке через пробел 
ADMIN_ID = ''

# телеграм_id технического админа, формат string
# получает технические сообщения бота
TECH = ''
```

## Запуск проекта через Docker

1. сбилдить образ через Dockerfile, загрузить на DockerHub

    ```bash
    docker build .
    docker push
    ```

2. Заполнить tbf поля в docker-compose.yml

3. Поднять контейнер

    ```bash
    docker compose up -d
    ```
