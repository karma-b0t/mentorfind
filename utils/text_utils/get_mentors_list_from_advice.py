import asyncio
import re
async def get_mentors_list_from_advice(advice: str):
    # Регулярное выражение для извлечения ников
    pattern = r"@([a-zA-Z0-9_]+)|https://t\.me/([a-zA-Z0-9_]+)"

    # Извлечение ников
    nicknames = []
    for contact in advice.split(' '):
        match = re.search(pattern, contact)
        if match:
            # Если найден @ник или ник из ссылки, добавляем в список
            nick = (match.group(1) or match.group(2))
            if nick not in nicknames:
                nicknames.append(nick)

 
    return nicknames