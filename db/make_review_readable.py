"""
 ["@seledkovti #seledkovti\n\nпришла к Тимуру с запросом на составление легенды. 
 мы поговорили про мой прошлый опыт до айти и нашли то, как преобразовать мой существующий опыт в айтишный. 
 выбрали несколько проектов, которые указали в резюме, и обсудили то, какие задачи я выполняла и какие технологии 
 использовала на данных проектах.\n\nтакже прошла у него мок-собес. за 2,5 часа мы успели обсудить hr-вопросы, 
 технические вопросы, а также пройти лайвкодинг. Тимур сразу давал обратную связь по заданным вопросам, 
 и советовал как лучше ответить на ту или иную тему.\n\nпланирую взять еще консультацию для более глубокого 
 разбора легенды. в целом рекомендую ментора)
 \n\nАвтор: @cllrdoor\n\n
 [**Найти/стать ментором**]
 (https://t.me/find_it_mentor_bot)
 [‌]
 (tg://user?msg_bot_data=1122811928)‌", 
 "@turbytale #turbytale\n\n
 Огромное спасибо ментору Тимуру @turbytale за консультацию.Рекомендую.Подсказал больше ожидаемого и 
 направил на правильный путь🙂
 \n\nАвтор: @VetalTZ\n\n
 [**Найти/стать ментором**](https://t.me/find_it_mentor_bot)
 [‌]
"""

import re

def clean_reviews(reviews):
    cleaned_reviews = ''
    for review in reviews:
        # Удаляем ссылки и текст в квадратных скобках
        review1 = re.sub(r"\[.*?\@]\(.*?\)", "", review)
        
        
        # Удаляем ссылки tg:// и другие URL
        review2 = re.sub(r"(https?://\S+|tg://\S+)", "", review1)
        
        # Убираем лишние переносы строк и пробелы
        review3 = re.sub(r"#\S+", "", review2)
        review4 = re.sub(r"@\S+", "", review3)
        review5 = re.sub(r"n\n\n\S", "", review4)
        review = re.sub(r"\n\n", "", review5)
        review = review.replace('\n\n', '')
        review = review.replace('Автор:', 'Отзыв: ')
        review = review.replace('[**Оставить отзыв**]', '')
        review = review.replace('(', '')
        review = review.replace('[**Найти ментора** |]', '')
        review = review.replace('Ментором**]', '')
        review = review.replace('ментором**] | [**Найти ментора**] |', '')
        review = review.replace('"', '')
        review = review.replace('[', '')
        review = review.replace(']', '')
        review = review.replace('[]', '')
        review = review.replace('[**Найти/стать ментором**]', '')
        review = review.replace('\n\n', '')
        review = review.replace('ментором**', '')
        review = review.replace('| **Найти ментора** |', '')
        review = review.replace('**Найти/стать', '')
        review = review.replace('\n\n', '')
        review = review.replace('|', '')
        # review = review.replace('  ', ' ')

        # print( review)
        # res = []
        # for sub in review1:
        #     res.append(re.sub('\n', '', sub))
        # print(res)
        # Выделяем автора
        # author_match = re.search(r"Автор: (@\w+)", review)
        # author = author_match.group(1) if author_match else "Unknown Author"
        
        # # Удаляем упоминание автора из текста
        # review_text = re.sub(r"Автор: (@\w+)", "", review)
        
        cleaned_reviews += review.strip()
    print(cleaned_reviews)
    
    return cleaned_reviews

# Пример списка отзывов
# with open('rate.txt', 'r', encoding='utf-8') as f:
#     reviews = f.readlines()

# # Чистим отзывы
# cleaned_reviews = clean_reviews(reviews)

# Выводим результат
# for review in cleaned_reviews:
#     print(f"Автор: {review['author']}")
#     print(f"Отзыв: {review['text']}\n")
