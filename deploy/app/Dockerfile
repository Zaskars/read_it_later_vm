FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PORT 8000
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./web/static /app/static/
COPY . /app/

CMD ["sh", "-c", "python manage.py migrate && node puppeteer/main && python manage.py runserver 0.0.0.0:$PORT && celery -A read_it_later worker -l info"]
