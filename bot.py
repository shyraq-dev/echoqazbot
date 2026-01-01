import asyncio
import os
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from dotenv import load_dotenv

# ------------------ Орта параметрлерін жүктеу ------------------
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ------------------ Router ------------------
router = Router()

# ------------------ /start пәрмені ------------------
@router.message(Command("start"))
async def cmd_start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Сәлемдесу", callback_data="hello")],
        [InlineKeyboardButton(text="ℹ️  Бот туралы", callback_data="info")]
    ])
    await message.answer(
        text=(
            f"Сәлем, <b>{message.from_user.first_name}</b>!\n\n"
            "Мен — <b>Эхо ботпын</b>. Не жазсаң да, соны қайталаймын. "
            "Төмендегі батырмаларды қолданып көр 👇"
        ),
        reply_markup=keyboard
    )

# ------------------ Inline батырма жауаптары ------------------
@router.callback_query(F.data == "hello")
async def say_hello(callback):
    await callback.message.answer("👋 Сәлем! Көңіл-күйің қалай?")
    await callback.answer()

@router.callback_query(F.data == "info")
async def show_info(callback):
    await callback.message.answer(
        "🤖 Бұл бот <b>Aiogram 3.22.0</b> негізінде жасалған.\n"
        "Функциялар:\n"
        "• Эхо жауап\n"
        "• /start пәрмені\n"
        "• Inline батырмалар\n"
        "• Typing эффекті"
    )
    await callback.answer()

# ------------------ Эхо-хендлер ------------------
@router.message(F.text)
async def echo_handler(message: Message, bot: Bot):
    # “теріп жатыр” эффекті
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(0.8)  # эффектті сәл күшейту үшін аз кідіріс
    await message.answer(message.text)

# ------------------ Негізгі функция ------------------
async def main():
    storage = MemoryStorage()

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )

    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    print("🤖 Эхо бот іске қосылды...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("⛔️ Бот тоқтатылды.")
