from telethon.sync import TelegramClient
import re

# Замени на реальные данные
api_id = ''
api_hash = ''
channel_username = -

# Создаем клиент с уникальным session_name
client = TelegramClient('session_name', api_id, api_hash)


def clean_review_text(review):
    # Remove unwanted elements using regular expressions
    review = re.sub(r'\n+', ' ', review)  # Replace multiple newlines with a space
    review = re.sub(r'Автор: @\w+', '', review)  # Remove author tags
    review = re.sub(r'\[.*?\]', '', review)  # Remove text within square brackets
    review = re.sub(r'\|', '', review)  # Remove pipe characters
    review = re.sub(r'https?://\S+', '', review)  # Remove URLs
    review = re.sub(r'\s+', ' ', review)  # Replace multiple spaces with a single space
    review = re.sub(r'\(\s*\(\s*\*\*\(', '', review)  # Remove pattern ( ( **(
    review = re.sub(r'\(\s*,', '', review)  # Remove pattern (,
    return review.strip()

async def search_reviews(full_name, keywords=None, exclude_patterns=None):
    async with client:
        # Ищем сообщения с именем и фамилией ментора
        messages = await client.get_messages(channel_username, search=full_name, limit=None)

        # Фильтруем сообщения по ключевым словам и исключающим паттернам
        filtered_messages = []
        for msg in messages:
            text = msg.text
            if full_name in text:
                if keywords:
                    if not any(keyword in text for keyword in keywords):
                        continue
                if exclude_patterns:
                    if any(re.search(pattern, text) for pattern in exclude_patterns):
                        continue
                filtered_messages.append(text)

        # Собираем текст всех отфильтрованных сообщений и чистим их
        reviews = [clean_review_text(msg) for msg in filtered_messages]
        # reviews = reviews[0].split('@')
        dict_reviews = {}
        for i, review in enumerate(reviews):
            dict_reviews[i] = review
        print(dict_reviews)
        return dict_reviews

import asyncio

if __name__ == '__main__':
    full_name = 'Андрей Кудинов'
    asyncio.run(search_reviews(full_name))
