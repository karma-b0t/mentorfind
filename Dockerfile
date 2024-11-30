# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1

# Команда для запуска приложения
CMD ["python", "webhook.py"]
