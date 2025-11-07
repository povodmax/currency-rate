# currency-rate

Hands-on experiments with modern technologies using real-world currency and cryptocurrency exchange rate data.

## Quick Start

```bash
poetry install
poetry run rates
```

## Stack
Python libraries:
```
openai
python-telegram-bot
requests
```

Services and tools:
- Railway
- Telegram

Production:
- Docker

## Details
Run Telegram bot in the background (without logs):
```bash
nohup python cyrates/bot/bot.py > /dev/null 2>&1 &
```
Pre-commit checks examples:
```bash
poetry run pre-commit run --files cyrates bot/bot.py
poetry run pre-commit run --all-files
```
Working with Docker locally:
- Go to the cloned project directory:
```bash
cd <path>/currency-rate
```
- Build the Docker image:
```bash
docker build -t crypto-bot .
```
- Run the bot with environment variables:
```bash
docker run --env-file .env crypto-bot
```

## Example .env file:
```
TELEGRAM_BOT_TOKEN=your_telegram_token
OPENAI_API_KEY=your_openai_api_key
```