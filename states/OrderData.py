from aiogram.dispatcher.filters.state import State, StatesGroup

class OrderForm(StatesGroup):
    waiting_for_details = State()
    waiting_for_location = State()
    waiting_for_contact = State()