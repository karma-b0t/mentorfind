from fastapi import FastAPI
from pydantic import BaseModel
from handlers import *
import requests
from decouple import config
from loguru import logger
from main import *
from tg_message_data import Update
from aiogram import F
from aiogram.fsm.storage.base import BaseStorage, StorageKey
from aiogram.fsm.context import FSMContext
from utils.states import UserStates, ChooseMentor

app = FastAPI()


class TelegramWebhook(BaseModel):
    message: dict = {}
    callback_query: dict = {}
    message: dict = {}
    pre_checkout_query: dict = {}
    success_payment: dict = {}


# Настройка логирования
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
#     handlers=[logging.FileHandler("webhook.log"), logging.StreamHandler()],
# )
# logger = logging.getLogger(__name__)


@app.post("/webhook")
async def webhook_handler(update: Update):
    logger.info(f"Received data: {update}")

    try:
        if update.message:
            key = StorageKey(
                bot_id=bot.id,
                chat_id=update.message.chat.id,
                user_id=update.message.from_user.id,
            )

            state = FSMContext(dp.storage, key)
            if update.message.text:
                text = update.message.text

                current_state = await state.get_state()
                # print('state from Message:', current_state)
                print("text:", text)
                if text == "/specialities_list":
                    await command_specialities_list(update.message, state)

                elif text == "/start":
                    await start(update.message, state)
                elif text == "/mentors_by_speciality":
                    await command_enter_speciality(update.message, state)

                elif current_state == UserStates().quiz_in_progress:
                    await quizz(update.message, state)

                elif current_state == ChooseMentor.choose_mentor:
                    if text.lower() == "да":
                        await state.set_state(ChooseMentor.mentor_chosen)
                        await mentor_chosen(update.message, state)
                    elif text.lower() == "нет":
                        await state.set_state(ChooseMentor.mentor_not_chosen)
                        await mentor_not_chosen(update.message, state)
                    else:
                        await got_wrong_data(update.message, state)
                        
                elif current_state == ChooseMentor.mentor_chosen:
                    await mentor_chosen(update.message, state)

                elif current_state == ChooseMentor.mentor_info:
                    await state.update_data(mentor_info=text)
                    await say_goodbye(update.message, state)
                else:
                    await pick_specific_speciality(update.message, state)

            elif update.message.document:
                await handle_docs(update.message, state)

        if update.callback_query:
            callback_query = update.callback_query
            callback_data = callback_query.data
            key = StorageKey(
                bot_id=bot.id,
                chat_id=callback_query.message.chat.id,
                user_id=callback_query.from_user.id,
            )

            state = FSMContext(dp.storage, key)
            current_state = await state.get_state()
            print("state from Callback:", current_state)
            if callback_data.startswith("start_quizz"):
                await state.set_state(UserStates().start_quizz.state)
                await state.clear()
                await start_quizz(callback_query, state)
            elif callback_data.startswith("upload_cv"):
                await bot.send_message(
                    callback_query.from_user.id,
                    text="Просто подгрузите свое резюме в формате .docx или .pdf",
                )
            elif callback_data.startswith("get_mentors_list_from_advice"):
                await get_mentors_list_from_advice(callback_query, state)
            if current_state == UserStates.get_mentors_list_by_specialities:
                if callback_data.startswith(
                    "page:"
                ):  # Обработка нажатия кнопок 'Next' и 'Previous'
                    await process_page_callback(callback_query, state)
                elif callback_data.startswith("mentor_id:"):
                    await get_mentor_info(callback_query, state)
                else:
                    await get_mentors_with_specialities(callback_query, state)
            elif (
                current_state == UserStates.get_mentor_info.state
            ):  # Обработка нажатия кнопки с имерем и рейтингом ментора
                if callback_data.startswith("speciality:"):
                    await get_mentors_with_specialities(callback_query, state)
                elif callback_data.startswith("reviews:"):
                    await send_mentors_reviews(callback_query, state, page=0)
                elif callback_data.startswith("page:"):
                    await send_mentors_reviews(callback_query, state)
                elif callback_data.startswith("mentor_id:"):
                    await get_mentor_info(callback_query, state)
            elif current_state == UserStates.get_specialities_list.state:
                if callback_data.startswith("speciality:"):
                    await get_mentors_with_specialities(callback_query, state)

        logger.info("Status: ok")
        return {"status": "ok"}

    except Exception as e:
        logger.exception(f"Error in webhook handler: {e}")
        return {"status": "error", "message": str(e)}


# обработчик для корневого URL
@app.get("/")
async def read_root():
    logger.info("Root endpoint reached")
    return {"message": "Welcome to the Telegram Webhook Server"}


# обработчик для favicon.ico
@app.get("/favicon.ico")
async def favicon():
    return {"status": "ok"}


if __name__ == "__main__":

    TOKEN = config("BOT_TOKEN")
    WEBHOOK_URL = config("WEBHOOK_URL")

    logger.info("TOKEN:", TOKEN)
    logger.info("WEBHOOK_URL:", WEBHOOK_URL)
    # Настройка вебхука
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    payload = {
        "url": f"{WEBHOOK_URL}/webhook",
        "allowed_updates": [
            "message",
            "callback_query",
            "pre_checkout_query",
            "successful_payment",
        ],
    }
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        logger.info("Webhook set successfully")
    else:
        logger.info(f"Failed to set webhook: {response.text}")

    # Запуск сервера FastAPI на порту 8000
    import uvicorn

    uvicorn.run("webhook:app", host="0.0.0.0", port=80, reload=True)
