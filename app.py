from aiogram import executor

import filters
import handlers
import middlewares
from utils.db_api.init_tables import create_tables
from loader import dp
from utils.notify_admins import on_startup_notify
from utils.schedular import init_schedular
from utils.set_bot_commands import set_default_commands
from utils.db_api.admin_data import laod_admins, ADMINS


async def on_startup(dispatcher):

    # 1) create tables
    await create_tables()

    # 2) load admins into ADMINS
    await laod_admins()
    print('Admins loaded')
    
    # 3)  Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)
    

    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    #start schedular
    await init_schedular()
    


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
