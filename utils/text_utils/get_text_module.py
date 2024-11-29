import asyncio
import json



async def get_text(key):
    
    with open("texts.json", 'r', encoding='utf-8') as f:
        texts = json.load(f)
    
        welcome_text = texts[key]
    return welcome_text

# if __name__ == '__main__':
#     asyncio.run(get_text('mentors_list_btn_text'))