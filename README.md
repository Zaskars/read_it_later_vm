`python -m venv env` - создание( для windows)

`env\Scripts\activate` - активация(для windows)

`pip install -r requirements.txt` - установка зависимостей

`django-admin startproject name` - создание проекта

`django-admin startapp web` - создание приложения

`python manage.py makemigrations` - подготовка миграций

`python manage.py migrate` - выполнение миграций

`node puppeteer/main` - запуск сервера на node

## Запуск фронтенда

- `cd web/static/web/ril_frontend` - перейти в папку фронтенда
- `npm i` - установить зависимости
- `npm run watch` - сборка для разработки
- `npm run build` - сборка для продакшена

## Запуск celery

- `celery -A read_it_later worker -l info`

## Запуск теллеграм бота

- `python manage.py telegram_bot`
