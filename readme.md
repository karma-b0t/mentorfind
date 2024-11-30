
## Local Run Prerequisites
- create `.env` file in the root directory
- fill-in following values:
```
BOT_TOKEN = 
DATABASE=
DB_HOST=
OPENAI_API_KEY = 
RESUME_ASSISTANT_ID = 
QUIZZ_ASSISTANT_ID = 
ROADMAP_ASSISTANT_ID = 
WEBHOOK_URL=
REDIS_URL = "redis://redis:6379/0"
```

- install `ngrok` tool

## Local Run with Docker
- run:
```
docker compose up --build
```


## Local Run
Для запуска приложения:

активируем venv

Из корня в терминале pip install -r requirements.txt

Копируем БД postgres, запоминаем password, database_name, host, port (5432), db_user, 

вставляем в переменные 

DATABASE="mentors"
DB_HOST="localhost"
DB_USER="postgres"
DB_PASSWORD="123"
DB_PORT="5432"
(подставляем свои)

Запускаем сервер ngrok командой ngrok http 8000

Копируем из терминала ngrok строку вида https://2379-212-58-102-223.ngrok-free.app, 

вставляем ее в файл .env в переменную  WEBHOOK_URL (полный выглядит так: )

запускаем redis server 

'redis-server' в терминале, если windows, сначала в терминале wsl

запускаем файл webhook  из корня (python3 -m webhook)

Пока так.