FROM python:3.11-slim

ENV POETRY_VERSION=1.8.2

# Установка Poetry
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

# Копируем проект (включая pyproject.toml, dummy_server.py и весь код)
COPY . .

# Установка зависимостей
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Команда запуска: бот + dummy Flask-сервер
CMD ["sh", "-c", "poetry run python cyrates/bot/bot.py & poetry run python cyrates/bot/dummy_server.py"]
