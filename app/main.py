import asyncio
import logging

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.ollama_handler import ollama_helper
from app.db_handler import PostgreSQLHandler
from config import settings

TOKEN = settings.BOT_TOKEN
logger = logging.getLogger(__name__)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        sql_text = ollama_helper.get_sql(message.text)
        result = sql_text

        logger.info(f"message: {message.text}, sql_text: {sql_text};")
        with PostgreSQLHandler(settings.DB_URI) as session:
            result = session.execute(query=sql_text)
        await message.answer(str(result.get(next(iter(result)))))
    except Exception as e:
        await message.answer(e)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(filename="sys_log.log", level=logging.INFO)
    asyncio.run(main())
