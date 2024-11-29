from aiogram import Bot, Dispatcher, Router
from aiogram.types import PreCheckoutQuery
from aiogram.fsm.storage.redis import RedisStorage
from decouple import config
# # Создание бота и диспетчера
TOKEN = config('BOT_TOKEN') 
REDIS_URL = config('REDIS_URL')
# print('Token for bot from Main.py', TOKEN)        # Сохраняем токен в переменную bot_token
bot = Bot(token=TOKEN)

storage = RedisStorage.from_url(REDIS_URL)
dp = Dispatcher(storage=storage)
router = Router()

# Определение обработчика pre_checkout_query
@router.pre_checkout_query()
async def pre_checkout_query_handler(pre_checkout_q: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)
