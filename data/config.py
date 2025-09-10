import os

from environs import Env
from utils.db_api.admin_data import ADMINS as superuser

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = superuser
IP = env.str("ip")  # Xosting ip manzili


