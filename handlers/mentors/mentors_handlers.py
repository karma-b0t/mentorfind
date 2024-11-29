import os
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
import asyncio
from tg_message_data import Message
from db import User, Mentor, GetDataFromDB, session
from aiogram.fsm.context import FSMContext
from utils.text_utils.get_text_module import get_text
from utils.files_utils.save_file import save_file, extract_text_from_file
from utils.ai_tools.get_mentor_by_resume import get_mentor_by_cv
from utils.ai_tools.get_mentor_by_quizz import get_advice_from_quizz
import logging
from main import dp, bot
from users import send_mentors_page
from main import *
from utils.states import UserStates, Quizz, ChooseMentor

# from utils import delete_message
from users import UserStates

async def command_quizz_for_mentor(message: Message, state: FSMContext):
    """
    Функция для вызова заполнения анкеты ментора
    """
    try:
        # print('command_specialities_list message:', message)
        await state.set_state(
            UserStates().get_specialities_list
        )  # Устанавливаем состояние для получения списка менторов по специальности
        # print('state:', state)

    except Exception as e:
        print("except on step set state command_specialities_list", e)
    try:

        specialities_list_btn_text = await get_text("mentors_list_btn_text")

        await bot.send_message(chat_id=message.chat.id, text="mentors_list_text")
        specialities_list = GetDataFromDB.get_specialities_list_from_json()

        await state.update_data(
            specialities_list
        )  # Сохраняем список специальностей в state (redis)
        btns = specialities_list
        inline_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=btn, callback_data=f"speciality: {btn}")]
                for btn in btns
            ]
        )
        await bot.send_message(
            chat_id=message.chat.id,
            text=specialities_list_btn_text,
            reply_markup=inline_kb,
        )

        # logger.info("Received help command from user ", message.chat.id)

    except Exception as e:
        print(e)
        # logger.exception("Error handling help command: ", e)
