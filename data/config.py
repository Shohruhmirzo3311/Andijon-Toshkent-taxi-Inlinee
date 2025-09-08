import os

from environs import Env

from data.group_id import SUPERUSERS

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = SUPERUSERS  # adminlar ro'yxati
# ADMINS = list(map(int, env.list("ADMINS")))
IP = env.str("ip")  # Xosting ip manzili




