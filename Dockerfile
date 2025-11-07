FROM python:3.11-slim

ENV POETRY_VERSION=1.8.2
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

# Копируем весь проект (включая pyproject.toml, код и всё остальное)
COPY . .

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Команда запуска
CMD ["poetry", "run", "python", "cyrates/bot/bot.py"]
