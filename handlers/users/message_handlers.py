import os
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from asyncio import sleep, create_task
from tg_message_data import Message
from db import GetDataFromDB, session
from aiogram.fsm.context import FSMContext
from utils.text_utils.get_text_module import get_text
from utils.files_utils.save_file import save_file, extract_text_from_word_file
from utils.ai_tools.get_mentor_by_resume import get_mentor_by_cv
from utils.ai_tools.get_mentor_by_quizz import get_advice_from_quizz
from utils import get_mentors_list_from_advice
import logging
from main import dp, bot
from .callback_handlers import send_mentors_page
from main import *
from utils.states import UserStates, ChooseMentor
from loguru import logger
from utils import UserStates


async def start(message: Message, state: FSMContext):
    """
    Handles the /start command by sending a welcome message with options to upload a resume
    or fill out a questionnaire.

    Args:
        message (Message): The incoming message object from the user.
        state (FSMContext): The finite state machine context for managing user states.

    Returns:
        None
    """
    await state.clear()
    text = await get_text("on_start_text")
    btns = [
        [InlineKeyboardButton(text="Загрузить резюме", callback_data="upload_cv")],
        [InlineKeyboardButton(text="Заполнить анкету", callback_data="start_quizz")],
    ]
    inline_kb = InlineKeyboardMarkup(inline_keyboard=btns)
    await bot.send_message(message.chat.id, text=text, reply_markup=inline_kb)


async def command_specialities_list(message: Message, state: FSMContext):
    """Handles the command to list specialities.
    This function sets the state to `get_specialities_list` to retrieve a list of mentors by speciality.
    It stores the list of specialities in the state.
    Args:
        message (Message): The incoming message object.
        state (FSMContext): The finite state machine context for managing user states.
    Raises:
        Exception: If there is an error setting the state or sending the message.
    Steps:
    1. Sets the state to `get_specialities_list`.
    2. Retrieves the button text for the specialities list.
    3. Sends a message to the user with the text "mentors_list_text".
    4. Retrieves the list of specialities from the database.
    5. Updates the state with the list of specialities.
    6. Creates an inline keyboard with buttons for each speciality.
    7. Sends a message to the user with the specialities list button text and the inline keyboard.
    """
    try:
        await state.set_state(
            UserStates.get_specialities_list
        )  # Устанавливаем состояние для получения списка менторов по специальности

    except Exception as e:
        logger.info("except on step set state command_specialities_list", e)
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

    except Exception as e:
        logger.info(e)


async def command_enter_speciality(message: Message, state: FSMContext):
    """
    Handles the /enter_speciality command from the user.
    This function retrieves a specific text message and sends it to the user.
    It then sets the state to `UserStates.specific_speciality` to prepare for
    receiving a list of mentors based on the user's speciality.
    Args:
        message (Message): The incoming message from the user.
        state (FSMContext): The current state of the finite state machine.
    Raises:
        Exception: If there is an error during the process, it will be caught and printed.
    """
    try:
        text = await get_text("specific_speciality_text")
        await bot.send_message(chat_id=message.chat.id, text=text)

        await state.set_state(
            UserStates.specific_speciality
        )  # Устанавливаем состояние для получения списка менторов по специальности
    except Exception as e:
        logger.info("except on step set state command_enter_speciality", e)


async def pick_specific_speciality(message: Message, state: FSMContext):
    """Handles the selection of a specific speciality from a list of specialities.
    Args:
        message (Message): The message object containing the user's input.
        state (FSMContext): The finite state machine context for managing user states.
    Functionality:
        - Sets the state to `UserStates.get_mentors_list_by_specialities`.
        - Retrieves the list of mentors for the selected speciality from the database.
        - Updates the state with the list of mentors and the selected speciality.
        - Sends the first page of mentors to the user.
    Exceptions:
        - Catches and prints any exceptions that occur while setting the state."""
    try:
        await state.set_state(
            UserStates.get_mentors_list_by_specialities
        )  # Устанавливаем состояние для получения списка менторов по специальности
    except Exception as e:
        logger.info("except on step set state pick_specific_speciality", e)
    speciality = message.text
    mentors_list = GetDataFromDB.get_mentors_by_speciality_from_db(
        session, speciality
    )  # Получаем список менторов по специальности

    await state.update_data(
        mentors_list=mentors_list, speciality=speciality
    )  # Сохраняем список специальностей в state (redis)
    await send_mentors_page(message, speciality, 0, state)


async def handle_docs(message: Message, state: FSMContext):
    """
    Handles the document sent by the user, processes it, and provides mentor advice.
    Args:
        message (Message): The message object containing the document sent by the user.
        state (FSMContext): The finite state machine context for maintaining the state.
    Workflow:
    1. Saves the document sent by the user and retrieves the file path and name.
    2. Sends a message to the user indicating that the document is being processed.
    3. Extracts text from the document and saves it to a .txt file.
    4. Obtains mentor advice based on the extracted text.
    5. Retrieves a list of mentors based on the advice and updates the state with this list.
    6. Sends the mentor advice to the user.
    7. Prompts the user to view more details about the mentors.
    8. Schedules a delayed message asking the user if they have chosen a mentor.
    9. Sets the state to `ChooseMentor.choose_mentor`.
    Returns:
        None
    """
    file_dox_path, file_name = await save_file(
        message
    )  # загружаем файл из ТГ, сохраняем в папку downloads, возвращаем путь к файлу WORD и имя 
    logger.info('file path from handle docs:', file_dox_path)
    wait_a_bit_text = await get_text("give_me_a_second")
    await bot.send_message(message.chat.id, text=wait_a_bit_text)
    file_txt_path = await extract_text_from_word_file(
        file_dox_path, file_name
    )  # сохраняем текст из файла в файл .txt, возвращаем путь к тексту
    advice = await get_mentor_by_cv(
        file_txt_path
    )  # Получаем совет от AI по тексту файла
    await handle_data_after_advice(advice, state, message)  #


async def delayed_message(bot, chat_id: int, delay: int, text: str, state: FSMContext):
    """
    Send a message to a specified chat after a delay.

    Args:
        bot: The bot instance to use for sending the message.
        chat_id (int): The ID of the chat where the message will be sent.
        delay (int): The delay in seconds before sending the message.
        text (str): The text of the message to be sent.

    Returns:
        None
    """
    await sleep(delay)
    
    await bot.send_message(chat_id=chat_id, text=text)
    await state.set_state(ChooseMentor.choose_mentor)


async def start_quizz(callback_query, state: FSMContext):
    """
    Initiates the quiz process for the user.

    This function sets the initial state for the quiz, updates the current question to the first one,
    retrieves the text for the first quiz question, and sends it to the user.

    Args:
        callback_query: The callback query object containing information about the user's interaction.
        state (FSMContext): The finite state machine context for managing user states.

    Returns:
        None
    """

    await state.set_state(UserStates.quiz_in_progress)
    await state.update_data(current_question=1)  # Устанавливаем начальный вопрос
    text = await get_text("quizz_1")
    await bot.send_message(
        chat_id=callback_query.from_user.id, text=text
    )  # Отправляем первый вопрос пользователю


async def quizz(message: Message, state: FSMContext):
    """
    Handles the quiz process for users by asking questions and collecting their answers.
    Args:
        message (Message): The message object containing the user's response.
        state (FSMContext): The finite state machine context for managing user state.
    Workflow:
        - Retrieves the current question number from the user's state data.
        - If there are more questions to ask (current question < 17):
            - Retrieves the text for the current question.
            - Updates the state with the user's answer to the current question.
            - Sends the next question to the user.
            - Increments the current question number in the state.
        - If the last question has been answered:
            - Sends a thank you message to the user.
            - Updates the state with the user's answer to the last question.
            - Retrieves advice based on the quiz answers and sends it to the user.
            - Schedules a delayed message asking if the user has chosen a mentor.
            - Sets the state to `ChooseMentor.choose_mentor` and asks if the user has chosen a mentor.
    Returns:
        None
    """
    user_data = await state.get_data()
    logger.info("user_data:", user_data)
    current_question = user_data.get("current_question", 1)

    # Проверяем, есть ли следующий вопрос
    if current_question < 5:
        previous_question_text = await get_text(f"quizz_{current_question}")
        data = await state.update_data(
            {
                f"question_{current_question}": previous_question_text,
                f"answer_{current_question}": message.text,
            }
        )
        next_question_text = await get_text(f"quizz_{current_question+1}")
        await bot.send_message(chat_id=message.chat.id, text=next_question_text)
        await state.update_data(current_question=current_question + 1)
    else:
        # Завершение анкеты после последнего вопроса
        await bot.send_message(
            chat_id=message.chat.id,
            text="Спасибо за ответы! Дайте мне немного времени, я подберу подходящего ментора!",
        )
        data = await state.update_data(
            {
                f"question_{current_question}": await get_text(
                    f"quizz_{current_question}"
                ),
                f"answer_{current_question}": message.text,
            }
        )
        print('data from quizz:', data)

        answer = await get_advice_from_quizz(data)
        await handle_data_after_advice(answer, state, message)


async def mentor_chosen(message: Message, state: FSMContext):
    """
    Handles the event when a mentor is chosen by the user.

    This function sets the state to `ChooseMentor.mentor_info` and sends a message
    to the user asking for the mentor's name and nickname.

    Args:
        message (Message): The message object containing information about the user's message.
        state (FSMContext): The finite state machine context for managing user states.

    Returns:
        None
    """
    await state.set_state(ChooseMentor.mentor_info)
    await bot.send_message(
        chat_id=message.chat.id, text="Напишите пожалуйста имя и ник ментора"
    )


async def mentor_not_chosen(message: Message, state: FSMContext):
    """
    Handles the case when a mentor is not chosen by the user.

    This asynchronous function sends a message to the user indicating that no mentor was chosen and prompts the user to select a mentor from the list. It then sets the state to `UserStates.get_specialities_list`.

    Args:
        message (Message): The incoming message object from the user.
        state (FSMContext): The finite state machine context for managing user states.

    Returns:
        None
    """
    await bot.send_message(
        chat_id=message.chat.id,
        text="Очень жаль! Давайте поищем еще! Выберите ментора из списка",
    )
    await state.set_state(UserStates.get_specialities_list)


async def say_goodbye(message: Message, state: FSMContext):
    """
    Asynchronously handles the goodbye message from the user.

    This function clears the current state of the FSMContext and sends a
    goodbye message to the user.

    Args:
        message (Message): The message object containing the user's message.
        state (FSMContext): The finite state machine context for the current user session.

    Returns:
        None
    """
    await state.clear()
    text = await get_text("thanks_for_answers")
    await bot.send_message(chat_id=message.chat.id, text=text)


async def handle_data_after_advice(advice, state, message):
    """
    Get mentors list from advice, set mentors list to the state,
    send message to user propose to watch information about every mentor in the list
    Create a task to send delayed message for ask user about his choice.

    Args:
        advice: text from AI
        message (Message): The message object containing the user's message.
        state (FSMContext): The finite state machine context for the current user session.
    """
    mentors_list = await get_mentors_list_from_advice(advice)
    logger.info("mentors_list:", mentors_list)
    await state.update_data(
        mentors_list_from_advice=mentors_list
    )

    links_list = await state.get_data()
    mentors_list_from_advice = links_list["mentors_list_from_advice"]
    found_mentors = False
    
    for link in mentors_list_from_advice:
        mentor_dict = GetDataFromDB.get_mentor_by_link_from_db(session, link)
        if mentor_dict is None:
            continue
            
        mentor = mentor_dict.get("description")
        mentor_id = mentor_dict.get("id")
        if mentor and mentor_id:
            found_mentors = True
            await state.set_state(UserStates.get_mentor_info)
            btn = InlineKeyboardButton(
                text="Посмотреть отзывы", callback_data=f"reviews: {mentor_id}"
            )
            await bot.send_message(
                message.chat.id,
                f"{mentor}",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[btn]]),
            )

    if not found_mentors:
        await bot.send_message(
            message.chat.id,
            "К сожалению, не удалось найти подходящих менторов. Попробуйте изменить критерии поиска."
        )
        return

    create_task(
        delayed_message(
            bot, message.chat.id, 300, await get_text("did_you_choose_mentor"), state
        )
    )

async def got_wrong_data(message: Message, state: FSMContext):
    """
    Handles the case when the user provides incorrect data.

    This asynchronous function sends a message to the user indicating that the data provided was incorrect and prompts the user to try again. It then sets the state to `UserStates.get_specialities_list`.

    Args:
        message (Message): The incoming message object from the user.
        state (FSMContext): The finite state machine context for managing user states.

    Returns:
        None
    """
    await bot.send_message(
        chat_id=message.chat.id,
        text="Извините, я не понял ваш ответ. Пожалуйста, попробуйте еще раз."
    )
    await state.set_state(UserStates.get_specialities_list)