from aiogram import Router, Bot, F
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from aiogram.fsm.context import FSMContext
from app.states.company import CompanyCreateCampaign
from app.dao.company import CompanyDAO
from app.dao.campaign import CampaignDAO
from app.messages.new_campaign import create_campaign_admin_message
from app.config import settings


router = Router()


@router.callback_query(F.data == "create_campaign")
async def create_campaign(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()
    await state.set_state(CompanyCreateCampaign.waiting_for_content_type)
    await callback.message.answer(
        "Последовательно заполните данные об анкете. \n Укажите типы контента"
    )


@router.message(CompanyCreateCampaign.waiting_for_content_type)
async def process_content_type(message: Message, state: FSMContext):
    content_type = message.text
    await state.update_data(content_type=content_type)
    await state.set_state(CompanyCreateCampaign.waiting_for_social_networks)
    await message.answer("Выберите социальные сети:")


@router.message(CompanyCreateCampaign.waiting_for_social_networks)
async def process_social_networks(message: Message, state: FSMContext):
    social_networks = message.text
    await state.update_data(social_networks=social_networks)
    await state.set_state(CompanyCreateCampaign.waiting_for_audience_priority)
    await message.answer("Выберите приоритет по аудитории (Мужская/Женская):")


@router.message(CompanyCreateCampaign.waiting_for_audience_priority)
async def process_audience_priority(message: Message, state: FSMContext):
    audience_priority = message.text
    await state.update_data(audience_priority=audience_priority)
    await state.set_state(CompanyCreateCampaign.waiting_for_product_type)
    await message.answer(
        "Что за продукт? (Например: Бренд одежды, Hr бренд или Салон красоты):"
    )


@router.message(CompanyCreateCampaign.waiting_for_product_type)
async def process_product_type(message: Message, state: FSMContext):
    product_type = message.text
    await state.update_data(product_type=product_type)
    await state.set_state(CompanyCreateCampaign.waiting_for_website_link)
    await message.answer("Введите ссылку на сайт или соцсеть (если есть):")


@router.message(CompanyCreateCampaign.waiting_for_website_link)
async def process_website_link(message: Message, state: FSMContext):
    website_link = message.text
    await state.update_data(website_link=website_link)
    await state.set_state(CompanyCreateCampaign.waiting_for_contact_method)
    await message.answer("Укажите способ связи (номер, почта или другое):")


@router.message(CompanyCreateCampaign.waiting_for_contact_method)
async def process_contact_method(message: Message, state: FSMContext):
    contact_method = message.text
    await state.update_data(contact_method=contact_method)
    await state.set_state(CompanyCreateCampaign.waiting_for_advertising_style)
    await message.answer(
        "Как вы хотите подавать информацию? (Нативно, рекомендация или детальный рассказ о продукте):"
    )


@router.message(CompanyCreateCampaign.waiting_for_advertising_style)
async def process_advertising_style(message: Message, state: FSMContext):
    advertising_style = message.text
    await state.update_data(advertising_style=advertising_style)
    await state.set_state(CompanyCreateCampaign.waiting_for_view_price)
    await message.answer(
        "Сколько вы платите за 1 просмотр? (Рекомендуем поставить 2р за просмотр):"
    )


@router.message(CompanyCreateCampaign.waiting_for_view_price)
async def process_view_price(message: Message, state: FSMContext):
    view_price = message.text
    await state.update_data(view_price=view_price)
    await state.set_state(CompanyCreateCampaign.waiting_for_check_submission)

    check_submission_button = InlineKeyboardButton(
        text="Отправить на проверку", callback_data="submit_for_check"
    )
    check_submission_markup = InlineKeyboardMarkup(
        inline_keyboard=[[check_submission_button]]
    )

    await message.answer(
        "Нажмите кнопку ниже, чтобы отправить рекламную кампанию на проверку.",
        reply_markup=check_submission_markup,
    )


# Обработчик нажатия на кнопку
@router.callback_query(
    CompanyCreateCampaign.waiting_for_check_submission,
    F.data == "submit_for_check",
)
async def process_check_submission(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    data = await state.get_data()
    view_price = data.get("view_price")

    await callback.message.edit_text(
        f"Рекламная компания уже проверяется, когда она будет проверена, вы будете проинформированы!"
    )

    data = await state.get_data()
    view_price = int(data.get("view_price"))
    description = {k: v for k, v in data.items() if k != "view_price"}

    telegram_id = callback.from_user.id

    company = await CompanyDAO.get_one_or_none(telegram_id=telegram_id)
    campaign = await CampaignDAO.create_campaign(
        company_id=company.id,
        description=description,
        view_price=view_price,
    )

    campaign_id = campaign.id

    username = callback.from_user.username
    full_name = callback.from_user.full_name

    # Формируем сообщение и клавиатуру для админского чата
    admin_message, admin_markup = create_campaign_admin_message(
        campaign_id=campaign_id,
        company_id=company.id,
        telegram_id=telegram_id,
        username=username,
        full_name=full_name,
        description=description,
        view_price=view_price,
    )

    await callback.bot.send_message(
        chat_id=settings.ADMIN_CHAT_ID, text=admin_message, reply_markup=admin_markup
    )

    # Очищаем состояние
    await state.clear()
