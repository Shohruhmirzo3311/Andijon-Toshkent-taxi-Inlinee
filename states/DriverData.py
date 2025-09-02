from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext



class DriverData(StatesGroup):
    ism = State()
    phone_number = State()
    car_number = State()
    account_id = State()


class DriverReg(StatesGroup):
    form = State()