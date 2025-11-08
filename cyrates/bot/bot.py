import os
import logging
import openai
from dotenv import load_dotenv
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from cyrates.parsing.extractor import CurrencyExtractor
from cyrates.parsing.prettyprint import pretty_print
from cyrates.bot import const

load_dotenv(override=True)

MENU, CHAT_MODE = range(2)  # constants for states of chat


def respect_answer(user: str) -> str:
    return f"{user}, what can I help you with?"


async def button_fiat_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Return fiat-rates by pressing 'Fiat-rates' button."""
    agent = CurrencyExtractor()
    result = pretty_print(agent.get_fiat_rates(), "image")
    await update.message.reply_photo(photo=result)
    await show_menu(update, context)  # return menu back


async def button_crypto_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Return crypto-rates by pressing 'Crypto-rates' button."""
    agent = CurrencyExtractor()
    result = pretty_print(agent.get_crypto_rates(), "image")
    await update.message.reply_photo(photo=result)
    # result = pretty_print(agent.get_crypto_rates(), "text")
    # await update.message.reply_text(result)
    await show_menu(update, context)  # return menu back


async def button_ai_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Activate chat-mode with AI by pressing 'AI-assistant'-button."""
    stop_button = [[KeyboardButton("stop")]]
    markup = ReplyKeyboardMarkup(stop_button, resize_keyboard=True)
    await update.message.reply_text(
        "Hi, I'm AI-assistant. " + respect_answer(update.effective_user.first_name), reply_markup=markup
    )
    return CHAT_MODE


async def stop_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Abort chat-mode with AI by pressing 'stop'-button."""
    await show_menu(update, context)
    return MENU


def get_chatgpt_response(user_message):
    try:
        # Send query to model
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": const.AI_ROLE},
                {"role": "user", "content": user_message},
            ],
            max_tokens=100,
            temperature=0.7,
        )
        # Get text answer
        chatgpt_message = response.choices[0].message.content.strip()
        return chatgpt_message
    except Exception as e:
        return f"Something went wrong while contacting AI: {str(e)}"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for text messages with AI."""
    user_message = update.message.text
    chatgpt_response = get_chatgpt_response(user_message)  # getting answer from ChatGPT
    await update.message.reply_text(chatgpt_response)  # send back to user


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show start menu with main buttons."""
    menu_buttons = [
        [KeyboardButton("Fiat-rates"), KeyboardButton("Crypto-rates")],
        [KeyboardButton("AI-assistant")],
    ]
    markup = ReplyKeyboardMarkup(menu_buttons, resize_keyboard=True)
    await update.message.reply_text(respect_answer(update.effective_user.first_name), reply_markup=markup)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start-command '/start'."""
    await update.message.reply_text(respect_answer(update.effective_user.first_name))
    await show_menu(update, context)
    return MENU


def main():
    """Bot launcher in polling or webhook mode."""

    mode = os.getenv("TELEGRAM_BOT_MODE").lower()

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN not set")
    
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

    application = Application.builder().token(token).build()

    # Register command handlers
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MENU: [
                MessageHandler(filters.Regex("^Fiat-rates$"), button_fiat_action),
                MessageHandler(filters.Regex("^Crypto-rates$"), button_crypto_action),
                MessageHandler(filters.Regex("^AI-assistant$"), button_ai_action),
            ],
            CHAT_MODE: [
                MessageHandler(filters.Regex("^stop$"), stop_chat),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    application.add_handler(conv_handler)

    # Logging configuration
    logging.basicConfig(level=logging.INFO)  # global logging level
    logging.getLogger("telegram.bot").setLevel(logging.WARNING)  # mute telegram.bot logs
    logging.getLogger("telegram.ext._application").setLevel(logging.WARNING)
    logger = logging.getLogger(__name__)

    # Bot launching
    logger.info(f"BOT launching in {mode} mode...")

    if mode == "webhook":
        webhook_url = os.getenv("WEBHOOK_URL")
        if not webhook_url:
            raise RuntimeError("WEBHOOK_URL must be set for webhook mode")
        application.run_webhook(
            listen="0.0.0.0",
            port=int(os.getenv("WEBHOOK_PORT")),
            webhook_url=webhook_url,
        )
    else:
        application.run_polling()


if __name__ == "__main__":
    main()
