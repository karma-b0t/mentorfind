from aiogram import Bot, types, Dispatcher
import asyncio
from aiogram.types import BotCommand
from decouple import config

BOT_TOKEN = config('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Определение списка команд
async def set_commands():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Определение списка команд
    commands = [
        BotCommand(command="/start", description="Старт"),
        BotCommand(command="/specialities_list", description="Список специальностей"),
        BotCommand(command="/mentors_by_speciality", description="Менторы по специальности"),
        BotCommand(command="/for_mentors", description="Стать ментором")

        
    ]

    # Установка списка команд
    await bot.set_my_commands(commands)
    print("Commands are set")

    # Закрываем сеанс после завершения работы
    await bot.session.close()# Запуск процесса установки команд
if __name__ == '__main__':
    asyncio.run(set_commands())
