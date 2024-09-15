import os
from dotenv import load_dotenv

load_dotenv()

# Токен Telegram-бота
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Базовый URL для взаимодействия с API
API_BASE_URL = os.getenv("API_BASE_URL")