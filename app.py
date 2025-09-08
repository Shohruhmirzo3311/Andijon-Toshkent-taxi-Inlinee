from aiogram import executor

import filters
import handlers
import middlewares
from data.init_tables import create_tables
from loader import dp
from utils.notify_admins import on_startup_notify
from utils.schedular import init_schedular
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)

    #create tables
    await create_tables()
    
    #start schedular
    await init_schedular()
    

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
