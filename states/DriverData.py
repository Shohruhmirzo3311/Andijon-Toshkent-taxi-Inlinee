from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class DriverData(StatesGroup):
    ism = State()
    phone = State()
    car = State()
    account_id = State()
    category = State()
    active_until = State()



class DriverReg(StatesGroup):
    form = State()


class AdminApprove(StatesGroup):
    days = State()
    
class DeleteDriver(StatesGroup):
    waiting_for_car_number = State()
    confirming_deletion = State()
    confirmation = State()
    

class UpdateDriver(StatesGroup):
    form = State()
    waiting_for_new_data = State()
    second = State()