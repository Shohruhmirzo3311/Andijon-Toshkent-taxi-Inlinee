import logging

from aiogram import Dispatcher
from utils.db_api.admin_data import ADMINS, laod_admins



async def on_startup_notify(dp: Dispatcher):
    admin_list = await laod_admins()
    
    for admin in admin_list:
        try:
            await dp.bot.send_message(admin, "Bot ishga tushdi")

        except Exception as err:
            logging.exception(err)

