import ast
from asyncio import sleep
import trace
import traceback
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from db import Mentor, GetDataFromDB, session
from aiogram.fsm.context import FSMContext
from tg_message_data.remake_data import Chat, Message, User
from utils.states import UserStates
from utils.text_utils.get_text_module import get_text
from main import bot
from loguru import logger


async def get_mentors_with_specialities(
    callback_query, state: FSMContext
):  # Первый шаг
    """Функция для получения списка менторов по общей специальности из списка. Первый шаг
    Устанавливаем состояние get_mentors_list_by_specialities для получения списка менторов по специальности
    Определяем специальность из callback data и сохраняем список менторов в state"""
    try:
        await state.set_state(UserStates.get_mentors_list_by_specialities)
        await state.set_state(UserStates.get_mentors_list_by_specialities)
    except Exception as e:
        logger.info("except on step set state get_mentors_with_specialities", e)
    # current_state = await state.get_state()
    speciality = callback_query.data.split(":")[
        1
    ].lstrip()  # Определим специальность из callback data
    text = await get_text("mentors_by_speciality_text")
    text += f" {speciality}"
    mentors_list = GetDataFromDB.get_mentors_by_speciality_from_json(
        session, speciality
    )
    await state.update_data(
        mentors_list=mentors_list, speciality=speciality
    )  # Сохраняем список менторов и общую выбранную специальность в state (redis)

    data = await state.get_data()

    # Отправляем первую страницу с запросом на выборку нужных менторов
    await send_mentors_page(callback_query, speciality, 0, state)


async def send_mentors_page(callback_query, speciality, page, state: FSMContext):
    """Функция для отображения страницы с менторами.
    Определяем номер страницы и специальность из callback data из прошлого шага get_mentors_with_specialities
    и отправляем страницу"""
    # current_state = await state.get_state()

    mentors_per_page = 7

    # Получаем список менторов для текущей страницы из базы данных
    mentors_list_from_state = await state.get_data()

    mentors_list = mentors_list_from_state["mentors_list"]

    total_mentors = len(mentors_list)
    total_pages = ((total_mentors - 1) // mentors_per_page) + 1

    btns = get_page_buttons(page, mentors_per_page, mentors_list)

    if page > 0 and page < (total_pages - 1):
        # Если обе кнопки "Previous" и "Next" должны отображаться
        btns.append(
            [
                InlineKeyboardButton(
                    text="Previous", callback_data=f"page:{page - 1}, {speciality}"
                ),
                InlineKeyboardButton(
                    text="Next", callback_data=f"page:{page + 1}, {speciality}"
                ),
            ]
        )
    elif page > 0:
        # Если только кнопка "Previous" должна отображаться
        btns.append(
            [
                InlineKeyboardButton(
                    text="Previous", callback_data=f"page:{page - 1}, {speciality}"
                )
            ]
        )
    elif page < (total_pages - 1):
        # Если только кнопка "Next" должна отображаться
        btns.append(
            [
                InlineKeyboardButton(
                    text="Next", callback_data=f"page:{page + 1}, {speciality}"
                )
            ]
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=btns)
    text = await get_text("mentors_by_speciality_text")
    text += f" {speciality}"
    # Если это первая страница, отправляем новое сообщение
    if page == 0:
        await bot.send_message(callback_query.from_user.id, text, reply_markup=keyboard)
    else:
        await bot.edit_message_reply_markup(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=keyboard,
        )


async def process_page_callback(callback_query, state: FSMContext):
    """Функция для обработки нажатия на кнопки 'Next' и 'Previous'"""

    page = int(
        callback_query.data.split(":")[1].split(", ")[0]
    )  # Определим номер страницы из callback data
    speciality = callback_query.data.split(":")[1].split(", ")[
        1
    ]  # Определим специальность из callback data
    # Проверяем текущее состояние и данные перед отправкой страницы
    data = await state.get_data()

    if "mentors_list" not in data:
        logger.info(
            "Список менторов отсутствует в состоянии. Возможно, произошла ошибка."
        )
        return
    # Отправляем новую страницу
    await send_mentors_page(callback_query, speciality, page, state)


def get_page_buttons(
    page, mentors_per_page, mentors_list
):  # Функция для создания кнопок с менторами
    """
    Функция для создания кнопок с менторами
    На вход получаем номер страницы, количество менторов на странице и список менторов
    Возвращаем список кнопок с менторами для текущей страницы"""

    start = int(page) * int(mentors_per_page)
    end = start + mentors_per_page
    btns = [
        [
            InlineKeyboardButton(
                text=f"{mentor['name']}, Специальность: \n{mentor['speciality']}",
                callback_data=f"mentor_id: {mentor['id']}",
            )
        ]
        for mentor in mentors_list[start:end]
    ]
    return btns


async def get_mentor_info(callback_query, state: FSMContext):
    MAX_MESSAGE_LENGTH = 4096
    MAX_DESCRIPTION_LENGTH = (
        1000  # описание может занимать до 1000 символов, так удобнее
    )

    """Функция для получения информации о менторе"""
    # current_state = await state.get_state()
    try:
        state_data = await state.get_data()
        speciality = state_data.get("speciality")
        logger.info("speciality from step get_mentor_info:", speciality)
        await state.set_state(
            UserStates.get_mentor_info
        )  # Устанавливаем состояние для получения информации о менторе
    except Exception as e:
        logger.info("except on step set state get_mentor_info", e)

    mentor_id = callback_query.data.split(": ")[1]
    telegram_id = callback_query.from_user.id
    mentor_info = GetDataFromDB.get_mentor_info_by_id_from_db(
        session, mentor_id
    )  # Получаем информацию о менторе
    text = await get_text("mentor_info_text")
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=(
                        f"speciality: {speciality}"
                        if speciality
                        else "get_mentors_list_from_advice"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    text="Посмотреть отзывы", callback_data=f"reviews: {mentor_id}"
                )
            ],
        ]
    )
    await bot.send_message(telegram_id, f"{mentor_info}", reply_markup=keyboard)


async def send_mentors_reviews(callback_query, state: FSMContext, page=0):
    """Функция для отправки отзывов о менторе"""

    await state.set_state(
        UserStates.get_mentor_info
    )  # Устанавливаем состояние для получения информации о менторе

    mentor_id = callback_query.data.split(": ")[1]
    telegram_id = callback_query.from_user.id
    reviews_str = GetDataFromDB.get_mentor_reviews_from_db(
        session, mentor_id
    )  # Получаем отзывы о менторе

    try:
        reviews_dict = ast.literal_eval(reviews_str)
    except (ValueError, SyntaxError) as e:
        logger.info(f"Ошибка при преобразовании строки в словарь: {e}")
        reviews_dict = {}

    # Если отзывов нет, отправляем сообщение
    if not reviews_dict:
        await bot.send_message(telegram_id, "У ментора нет отзывов")
        return

    # Проход по ключам словаря и получение отзывов
    reviews_sent = 0
    try:
        for review in reviews_dict.values():
            if reviews_sent > 4:
                break
            if review:
                await bot.send_message(telegram_id, f"{review}")
                reviews_sent += 1
                await sleep(1)

    except Exception as e:
        logger.info(f"Ошибка при получении отзывов: {e}")
        traceback.print_exc()
        await bot.send_message(
            telegram_id, "Кажется, возникла ошибка при получении отзывов."
        )

    # Кнопки для возврата
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Назад", callback_data=f"mentor_id: {mentor_id}"
                )
            ],
        ]
    )
    await bot.send_message(
        telegram_id, text="Назад к информации о менторе", reply_markup=keyboard
    )


async def get_mentors_list_from_advice(callback_query, state: FSMContext):
    """Функция для получения списка менторов по совету от AI"""
    links_list = await state.get_data()
    mentors_list_from_advice = links_list["mentors_list_from_advice"]

    for link in mentors_list_from_advice:
        mentor_dict = GetDataFromDB.get_mentor_by_link_from_db(session, link)
        mentor = mentor_dict.get("description")
        mentor_id = mentor_dict.get("id")
        callback_query.data = f"id: {mentor_id}"
        await state.set_state(UserStates.get_mentor_info)
        btn = InlineKeyboardButton(
            text="Посмотреть отзывы", callback_data=f"reviews: {mentor_id}"
        )
        await bot.send_message(
            callback_query.from_user.id,
            f"{mentor}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[btn]]),
        )
