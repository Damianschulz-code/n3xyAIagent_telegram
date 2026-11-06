import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings
from database import Database
from ai_client import AIClient

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("n3xy")

db = Database(settings.database_path)
ai = AIClient(settings)
dp = Dispatcher()

WELCOME = (
    "Привет! Я N3XY AI — демонстрационный Telegram AI-агент.\n\n"
    "Просто напиши мне сообщение, и я отвечу.\n"
    "Команды:\n"
    "/help — помощь\n"
    "/reset — очистить контекст диалога\n"
    "/about — информация о проекте"
)

@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    await db.ensure_user(message.from_user.id)
    await message.answer(WELCOME)

@dp.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer(
        "Отправь обычное текстовое сообщение, чтобы начать диалог.\n\n"
        "Команды:\n"
        "/reset — начать новый диалог\n"
        "/about — информация о боте"
    )

@dp.message(Command("about"))
async def about_handler(message: Message) -> None:
    await message.answer(
        "<b>N3XY AI Agent</b>\n"
        "Демонстрационный проект Telegram-агента на Python.\n"
        "Стек: Aiogram 3, OpenAI-compatible API, SQLite, Docker."
    )

@dp.message(Command("reset"))
async def reset_handler(message: Message) -> None:
    await db.clear_history(message.from_user.id)
    await message.answer("Контекст диалога очищен. Можем начать заново.")

@dp.message(F.text)
async def chat_handler(message: Message) -> None:
    user_id = message.from_user.id
    text = (message.text or "").strip()

    if not text:
        return
    if len(text) > settings.max_message_length:
        await message.answer(
            f"Сообщение слишком длинное. Максимум: {settings.max_message_length} символов."
        )
        return

    await db.ensure_user(user_id)
    await db.add_message(user_id, "user", text)

    status = await message.answer("Думаю…")
    try:
        history = await db.get_history(user_id, settings.history_limit)
        answer = await ai.complete(history)
        await db.add_message(user_id, "assistant", answer)
        # Telegram message limit is 4096 characters.
        await status.edit_text(answer[:4000])
    except Exception:
        logger.exception("AI request failed for user_id=%s", user_id)
        await status.edit_text(
            "Не получилось получить ответ от AI-сервиса. Попробуй немного позже."
        )

@dp.message()
async def unsupported_handler(message: Message) -> None:
    await message.answer("Пока я умею обрабатывать только текстовые сообщения.")

async def main() -> None:
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured")
    await db.initialize()
    bot = Bot(
        token=settings.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    logger.info("Starting N3XY AI Agent")
    try:
        await dp.start_polling(bot)
    finally:
        await ai.close()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
