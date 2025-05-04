from aiogram.fsm.state import State, StatesGroup


class AdminRejectBlogger(StatesGroup):
    waiting_for_reason_blogger = State()


class AdminRejectCampaign(StatesGroup):
    waiting_for_reason_campaign = State()


class AdminRejectIntegration(StatesGroup):
    waiting_for_reason_integration = State()
