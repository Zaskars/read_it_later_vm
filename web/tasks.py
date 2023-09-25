import asyncio

from aiogram import Bot
from celery.signals import task_success, task_failure

from read_it_later.celery import app
from read_it_later.settings import TELEGRAM_BOT_TOKEN
from web.models import User
from web.services.save_article import save

bot = Bot(token=TELEGRAM_BOT_TOKEN)


@app.task
def save_pdf(url, user_id=None):
    tg_id = None

    if user_id:
        user = User.objects.all().filter(id=user_id)
        if not user:
            tg_id = user_id
            user = User.objects.all().filter(telegram_user_id=tg_id)
            if not user:
                raise AttributeError(f"Don't find user with user_id = {user_id} or telegram_user_id = {user_id}")
            else:
                user = user[0]
        else:
            user = user[0]
    else:
        raise AttributeError('Attribute user_id not found')

    save(url, user)

    return {'tg_id': tg_id, 'url': url}


@task_success.connect
def task_done(sender=None, result=None, **kwargs):
    tg_id = result.get('tg_id')
    if tg_id:
        asyncio.run(send_message(chat_id=tg_id, text=f"Статья {result['url']} успешно сохранена."))


async def send_message(chat_id, text):
    await bot.send_message(chat_id=chat_id, text=text)


@task_failure.connect
def send_failure_message(sender=None, result=None, **kwargs):
    tg_id = result.get('tg_id')
    if tg_id:
        asyncio.run(
            send_message(
                chat_id=tg_id,
                text=f"Не удалось сохранить статью {result['url']}. Возможно сервис read it later не "
                     "может сохранить эту статью. Попробуйте сделать это на сайте."
            )
        )
