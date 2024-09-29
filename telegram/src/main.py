import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from aiogram.fsm.storage.memory import MemoryStorage

router = Router()
storage = MemoryStorage()
load_dotenv()
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

async def main():
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()

    greeting = """Здравствуйте!
    Это бот команды Гроза по кейсу «Rutube-Интеллектуальный помощник».
    
    Чтобы получить ответ из базы знаний, просто введите ваш запрос."""

    await message.answer(greeting)

@router.message()
async def conversation(message: types.Message, state: FSMContext):
    user_input = message.text
    answer = get_answer(user_input)

    await message.answer(answer)


@router.message(Command("stop"))
async def cmd_start(message: types.Message, state: FSMContext, bot):
    msg = """
    Вы остановили работу бота. Нажмите /start, чтобы начать сначала.
    """

    await message.answer(msg)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")