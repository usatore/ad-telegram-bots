from aiogram.fsm.state import default_state, State, StatesGroup


class CampaignCreationStates(StatesGroup):
    # Этапы для ввода информации рекламной кампании
    waiting_for_content_type = State()  # Тип контента (Текст и Видео)
    waiting_for_social_networks = State()  # Социальные сети
    waiting_for_audience_priority = State()  # Приоритет по аудитории
    waiting_for_product_type = State()  # Тип продукта
    waiting_for_website_link = State()  # Ссылка на сайт или соцсеть
    waiting_for_contact_method = State()  # Способ связи
    waiting_for_advertising_style = State()  # Как подавать информацию
    waiting_for_view_price = State()  # Сколько платят за 1 просмотр
    waiting_for_check_submission = State()  # Когда компания отправлена на проверку


class AdminStates(StatesGroup):
    waiting_for_input_reason = State()  # Новое состояние для причины отклонения
