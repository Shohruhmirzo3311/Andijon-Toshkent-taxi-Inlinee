from aiogram.utils.callback_data import CallbackData

driver_callback = CallbackData("command", "action")

bot_callback = CallbackData("bot", "action")

client_callback = CallbackData("client", "route")

worker_callback = CallbackData("worker", "task" )

admin_driver_callback = CallbackData("adm", "a", "id")
driver_deletion_callback = CallbackData("command", "action", "car_number")