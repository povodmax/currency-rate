# currency-rate
Hands-on experiments with various technologies using real-world currency exchange rate data.

# Quick-start
1. poetry install
2. poetry run rates

# Background execution Telegram-bot (without logs)
nohup python cyrates/bot/bot.py > /dev/null 2>&1 &

# Pre-commit checks example
poetry run pre-commit run --files bot/bot.py 
pre-commit run --all-files 