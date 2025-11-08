FROM python:3.11-slim

ENV POETRY_VERSION=1.8.2

# Установка Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Рабочая директория
WORKDIR /app

# Копируем проект (включая pyproject.toml и весь код)
COPY . .

# Установка зависимостей
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Открываем порт для webhook-сервера
EXPOSE 8080

# Команда запуска
CMD ["poetry", "run", "python", "cyrates/bot/bot.py"]
