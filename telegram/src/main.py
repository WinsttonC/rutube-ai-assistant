import asyncio
import logging
import os

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from api.fetch_prediction import fetch_prediction
from models import PredictRequest
from const import TELEGRAM_BOT_TOKEN

router = Router()
storage = MemoryStorage()

async def main():
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    bot = Bot(TELEGRAM_BOT_TOKEN)
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
    if user_input:
        try:
            response = await fetch_prediction(PredictRequest(question=user_input))
            answer = response.answer
            cls_1 = f'Классификатор 1 уровня: {response.class_1}'
            cls_2 = f'Классификатор 2 уровня: {response.class_2}'
            response = f'{answer}\n\n{cls_1}\n{cls_2}'

        except Exception as e:
            response = "Произошла ошибка"
            raise e
        await message.answer(response)


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
