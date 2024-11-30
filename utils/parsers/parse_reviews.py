from telethon.sync import TelegramClient
import re
from decouple import config

# Get config values
api_id = config("api_id")
api_hash = config("api_hash")
channel_username = config("channel_username")

def clean_review_text(review):
    # remove links and PII from reviews texts
    review = re.sub(r'\n+', ' ', review)
    review = re.sub(r'Автор: @\w+', '', review)
    review = re.sub(r'\[.*?\]', '', review)
    review = re.sub(r'\|', '', review)
    review = re.sub(r'https?://\S+', '', review)
    review = re.sub(r'\s+', ' ', review)
    review = re.sub(r'\(\s*\(\s*\*\*\(', '', review)
    review = re.sub(r'\(\s*,', '', review)
    return review.strip()

async def search_reviews(full_name, keywords=None, exclude_patterns=None):
    # Create a new client instance for each request
    async with TelegramClient(f'session_{full_name}', api_id, api_hash) as client:
        # Search for messages with mentor name
        messages = await client.get_messages(channel_username, search=full_name, limit=None)

        # Filter messages
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

        # Clean and format reviews
        reviews = [clean_review_text(msg) for msg in filtered_messages]
        dict_reviews = {i: review for i, review in enumerate(reviews)}
        print(dict_reviews)
        return dict_reviews

import asyncio

if __name__ == '__main__':
    full_name = 'Андрей Кудинов'
#     asyncio.run(search_reviews(full_name))