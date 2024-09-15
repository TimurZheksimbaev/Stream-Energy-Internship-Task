import logging
from logging.handlers import TimedRotatingFileHandler

# Настройка логгера
logger = logging.getLogger('app_logger')
logger.setLevel(logging.INFO)

# Ротация логов по дате (ежедневно)
handler = TimedRotatingFileHandler('logs/app.log', when='midnight', interval=1)
handler.suffix = "%Y-%m-%d"  # Формат для имен файлов с датой
handler.setLevel(logging.INFO)

# Форматирование логов
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Добавляем хендлер к логгеру
logger.addHandler(handler)


def log_user_action(user: str, action: str):
    logger.info(f"User: {user} Made action: {action}")

def log_error(error: str):
    logger.error(error)