from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from logger import log_user_action, log_error
from config.read_env import TOKEN_SECRET, TOKEN_ALGORITHM, TOKEN_EXPIRATION

# Конфигурация для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функции для работы с паролями
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Функция для создания JWT токена
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, TOKEN_SECRET, algorithm=TOKEN_ALGORITHM)
    log_user_action(data.get("sub"), f"Created access token")
    return encoded_jwt

# Функция для валидации токена
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, TOKEN_SECRET, algorithms=[TOKEN_ALGORITHM])
        log_user_action(payload.get("sub"), f"Decoded access token")
        return payload
    except JWTError:
        return None
