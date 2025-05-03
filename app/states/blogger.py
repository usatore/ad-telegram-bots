from aiogram.fsm.state import State, StatesGroup


class BloggerSendProfileLinks(StatesGroup):
    waiting_for_profile_links = State()


class BloggerCreateIntegration(StatesGroup):
    waiting_for_load_materials = State()
    waiting_for_submit_materials = State()
