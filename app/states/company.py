from aiogram.fsm.state import State, StatesGroup


class CompanyAddDeposit(StatesGroup):
    waiting_for_deposit_amount = State()