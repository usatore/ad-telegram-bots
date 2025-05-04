from aiogram.fsm.state import State, StatesGroup


class AdminRejectBlogger(StatesGroup):
    waiting_for_reason = State()


class AdminRejectCampaign(StatesGroup):
    waiting_for_reason = State()


class AdminRejectIntegration(StatesGroup):
    waiting_for_reason = State()
