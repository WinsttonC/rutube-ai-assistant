import asyncio
import logging
from api.fetch_prediction import fetch_prediction
from aiogram import Bot, Dispatcher, types
from models import PredictRequest
from const import TELEGRAM_BOT_TOKEN
from aiogram.filters.command import Command

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)
# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

    # Хэндлер на команду /start


@dp.message()
async def echo(message: types.Message):
    if message.text:
        try:
            response = await fetch_prediction(PredictRequest(question=message.text))
            response = response.answer
        except Exception as e:
            response = "Произошла ошибка"
            raise e
        await message.answer(response)


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
