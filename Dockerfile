# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /mentor_bot

# Копируем файлы проекта в контейнер
COPY . /mentor_bot

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1

# Команда для запуска приложения
CMD ["python", "webhook.py"]