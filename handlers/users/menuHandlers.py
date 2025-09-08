from aiogram import types
from aiogram.dispatcher.filters import Command, Text

from keyboards.default.startMenu import Startmenu
from keyboards.inline.menuKeyboard import bot_action_menu, driver_action_menu
from loader import dp


@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    await message.answer("Asosiy menu", reply_markup=Startmenu)




@dp.message_handler(text_contains="🚕 Haydovchilar")
async def show_driver_actions(message: types.Message):
    await message.answer("Haydovchilar bo'limi", reply_markup=driver_action_menu)


@dp.message_handler(text_contains="🤖 Bot")
async def show_bot_actions(message: types.Message):
    await message.answer("Bot bo'limi", reply_markup=bot_action_menu)