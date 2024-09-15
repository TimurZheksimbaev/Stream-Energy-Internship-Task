from loguru import logger

logger.add("logs/bot.log", rotation="1 day", retention="7 days", level="INFO")
