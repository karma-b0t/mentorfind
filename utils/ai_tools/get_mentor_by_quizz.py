from openai import OpenAI
from decouple import config

OPENAI_API_KEY = config("OPENAI_API_KEY")
assistant_id = config("QUIZZ_ASSISTANT_ID")


async def get_advice_from_quizz(input_text):
    input_text = str(input_text)
    client = OpenAI(api_key=OPENAI_API_KEY)
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                # "content": "Павел Кирсанов PYTHON – DEVELOPER | kirsanov118 @gmail.com |  GitHub | LinkedIn | Tbilisi Telegram @kirsanov69 | WhatsApp +995 595 510 542 Python-разработчик с 1,5 годами коммерческого опыта. Увлечён созданием приложений, которые решают реальные задачи. Постоянно учусь и совершенствую свои навыки. Мой предыдущий опыт в строительной инженерии помогает мне подходить к задачам структурированно. Ключевые навыки Python - Django - Flask - FastAPI - Asyncio - PostgreSQL - SQLite - Django ORM - SQLAlchemy - Git - Telegram API - Pandas - NumPy - Rasa - spaCy - Linux - WebSocket - AWS - aiogram - aiohttp - APScheduler - beautifulsoup4 - fiona - geopandas - geopy - osmnx - shapely - pyproj - gTTS - pyttsx3 - httpx - requests - python-dotenv - python-telegram-bot - Pydantic - Tornado - lxml Опыт работы BFL Robots, Тбилиси Разработчик чат-ботов [Январь 2023 – Август 2024] https://t.me/Self_guide_bot Разработал Telegram-бота, который получает геолокацию пользователя, строит маршруты и отправляет фото и аудиофайл при достижении точки назначения. Интегрировал GPT-4 для улучшения текста и Google TTS для преобразования текста в речь. Разработал и внедрил серверную часть для обработки вебхуков; проект был развернут на AWS. Разработал Telegram-бота для помощи клиентам управляющих компаний в автоматизации обработки запросов на обслуживание, оплату и техническую поддержку. Разрабатывал скрипты для голосовых ботов, обучал модели с использованием Rasa и spaCy. Определял и внедрял пользовательские воронки с использованием конечных автоматов состояний (FSM). Редактировал диалоги, устранял ошибки и решал технические проблемы. Участвовал в проектировании архитектуры приложения с нуля. Управлял полным циклом разработки — от идеи до запуска, включая разработку, тестирование и развертывание на AWS Технологии: Python, FastAPI, Asyncio, OpenAI API, Google TTS, AWS, Telegram API, Nginx, Certbot, OpenStreetMaps API,  SQLAlchemy, PostgreSQL,  WikiAPI. До этого больше 15 лет работал в строительстве - прошел путь от рабочего до директора собственной фирмы. Пет-проекты Хакатон от Latoken (1-е место), Сентябрь 2024:**  Срок разработки - 1 день. Разработка Telegram-бота с использованием OpenAI API и Aiogram. Бот успешно интегрировал модель ChatGPT, обученную мной на данных о компании Latoken, для предоставления пользователям персонализированной информации и ответов на вопросы. Реализовал функционал интерактивного обучения пользователей с помощью квизов и опросов. Обеспечил продвижение хакатона внутри бота. Flask — Приложение для управления семейным бюджетом GITHUB Разработал приложение для управления расходами с визуализацией данных (Pandas) и хранением информации в SQLite. Django — Простые веб-приложения GITHUB Создал несколько веб-приложений после прохождения курса на Stepik по Django. .GitHub: GitHub LinkedIn: LinkedIn Английский: уровень B1-В2",
                "content": input_text,
                # Attach the new file to the message.
                # "attachments": [
                #     {"file_id": message_file.id, "tools": [{"type": "file_search"}]}
                # ],
            }
        ]
    )

    # The thread now has a vector store with that file in its tool resources.
    print("thread.tool_resources.file_search", thread.tool_resources.file_search)

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant_id
    )

    messages = list(
        client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id)
    )

    message_content = messages[0].content[0].text
    annotations = message_content.annotations
    citations = []
    for index, annotation in enumerate(annotations):
        message_content.value = message_content.value.replace(
            annotation.text, f"[{index}]"
        )
        if file_citation := getattr(annotation, "file_citation", None):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(f"[{index}] {cited_file.filename}")

    print("message_content.value", message_content.value)
    print("\n".join(citations))
    return message_content.value


# if __name__ == "__main__":
#     text = "{'current_question': 16, 'question_1': 'Что вы хотите получить от менторства? (повышение квалификации, смена работы, подготовка к собеседованиям и т.д.)', 'answer_1': 'повысить грейд до мидла и найти работу', 'question_2': 'Какие конкретные навыки или знания вы хотите развить?', 'answer_2': 'Не знаю, для этого мне и нужен ментор', 'question_3': ' Каких результатов вы ожидаете в итоге?', 'answer_3': 'найти работу с достойной зп', 'question_4': 'Текущий уровень знаний и опыта: В какой области IT вы работаете сейчас?', 'answer_4': 'Телеграм боты, Django', 'question_5': 'С какими задачами вы уже справлялись в своей сфере?', 'answer_5': 'Успешно интегрировал разные API, поднимал сервер, работал с ORM - Alchemy, Django, деплой и разработка телеграм ботов под ключ', 'question_6': 'Каков ваш опыт работы в этой сфере?', 'answer_6': '2 года', 'question_7': 'Какие технологии вы уже знаете на уровне продвинутого пользователя?', 'answer_7': 'Django, Aiogram', 'question_8': 'Какие технологии вы хотите изучить?', 'answer_8': 'Те, которые нужны для уровня Мидл', 'question_9': 'Предпочтения по ментору: Какая специализация ментора вас интересует больше всего?', 'answer_9': 'python', 'question_10': 'Какой опыт работы у ментора должен быть?', 'answer_10': 'неважно', 'question_11': 'Предпочитаете ли вы ментора с академическим образованием или большим практическим опытом?', 'answer_11': 'неважно', 'question_12': 'Важны ли для вас отзывы других пользователей о менторе?  Какие критерии в отзывах кажутся вам важными для выбора? (например, отзывчивость, профессионализм, умение объяснять).', 'answer_12': 'отзывчивость, профессионализм, умение объяснять', 'question_13': 'Доступность и формат работы: Какая форма менторства вам подходит больше всего (онлайн, офлайн, комбинированный формат)?', 'answer_13': 'онлайн', 'question_14': 'Какова оптимальная длительность одной сессии, чтобы вы успевали усвоить информацию, но не чувствовали перегрузку?', 'answer_14': '1-2 часа', 'question_15': 'Какая частота встреч вам подходит?', 'answer_15': '1-2 раза в неделю', 'question_16': 'Каков ваш бюджет на менторство?', 'answer_16': '100000'}"
#     get_advice_from_quizz(text)