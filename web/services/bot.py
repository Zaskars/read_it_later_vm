from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.redis import RedisStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.markdown import hlink

from read_it_later.settings import TELEGRAM_BOT_TOKEN
from web.models import TelegramHash
from web.tasks import save_pdf

redis_host = '0.0.0.0'
redis_port = '6379'
redis_db = 0

storage = RedisStorage(host=redis_host, port=redis_port, db=redis_db)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=storage)


class SendLink(StatesGroup):
    waiting_link = State()


@dp.message_handler(commands=['start'], state='*')
async def start_handler(message: types.Message, state: FSMContext):
    await state.finish()

    user_full_name = message.from_user.full_name

    await message.answer(f"Привет, {user_full_name}. Я бот для взаимодействия с ресурсом read it later")

    text = message.text

    try:
        hash = text.split(" ")[1]
    except IndexError:
        await message.answer(f"Для подключения аккаунта на сайте перейдите по ссылке в профиле")
        return

    telegram_hash = TelegramHash.objects.get(hash=hash)
    telegram_hash.user.telegram_user_id = message.from_user.id
    telegram_hash.user.save()

    await message.answer(
        f"Вы вошли как {telegram_hash.user.email}. "
        "Отправьте ссылку на статью, которую хотите сохранить"
    )

    await SendLink.waiting_link.set()
    telegram_hash.delete()


@dp.message_handler(commands=['help'], state='*')
async def help(message: types.Message):
    await message.answer(
        "Я бот для взаимодействия с ресурсом read it later. Вы можете отправить мне ссылку "
        "на статью, чтобы я сохранил ее в ваш аккаунт. "
        f"Для работы со мной, Вы должны быть зарегистрированны на {hlink('сайте', url='http://127.0.0.1:8000/')}\n\n",
        parse_mode='HTML'
    )


@dp.message_handler(state=SendLink.waiting_link)
async def send_link_to_ril(message: types.Message, state: FSMContext):
    if message.text[:4] != 'http':
        await message.answer("Пожалуйста, введите валидный url адрес")
        return

    await message.answer('Ссылка отправлена сайту на обработку')

    save_pdf.delay(url=message.text, user_id=message.from_user.id)

    await message.answer(
        'Ссылка успешно обработана. Можете отправить следующую ссылку'
    )


def start_bot():
    executor.start_polling(dp)


if __name__ == '__main__':
    start_bot()
