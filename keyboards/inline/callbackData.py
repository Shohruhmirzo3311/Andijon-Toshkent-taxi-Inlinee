from aiogram.utils.callback_data import CallbackData

driver_callback = CallbackData("command", "action")

bot_callback = CallbackData("bot", "action")

client_callback = CallbackData("client", "route")

worker_callback = CallbackData("worker", "task" )