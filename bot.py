import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# Telegram Bot Token (Replace with your actual token)
TOKEN = "YOUR_BOT_TOKEN_HERE"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("ሰላም! የኬበር እቁብ ቦት በሰላም ተጀምሯል።")

# Receipt handling example
@dp.message(F.photo)
async def handle_receipt(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    photo_file_id = message.photo[-1].file_id
    
    # Approval keyboard
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="✅ ክፍያው ተረጋግጧል (አክቲቭ አድርግ)",
                    callback_data=f"approve_{user_id}"
                )
            ]
        ]
    )
    await message.answer(f"ደረሰኝ ከ {user_name} ደርሷል። እባክዎ ያረጋግጡ።", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())