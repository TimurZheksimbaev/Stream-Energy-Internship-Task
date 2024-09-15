import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Настройка логирования
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(pathname)s - %(message)s')

# Создание логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Настройка ротации логов
log_file = f"logs/app/app_{datetime.now().strftime('%Y-%m-%d')}.log"
file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

# Логирование в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)


def log_user_action(user: str, message: str):
    logger.info(f"User: {user} Action: {message}")

def log_error(message: str):
    logger.error(message)