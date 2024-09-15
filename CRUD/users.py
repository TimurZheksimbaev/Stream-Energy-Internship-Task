from datetime import timedelta
from typing import Dict

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import Session
from database.init_database import get_db
from models.models import User
from middleware.middleware import get_password_hash, verify_password, create_access_token, decode_access_token
from schemas.user import CreateUser
from schemas.token import Token
from loggers.logger import logger
from exceptions import UserAlreadyExistsException, IncorrectCredentialsException, ValidateCredentialsException

# Регистрация пользователя
async def create_user(db: AsyncSession, user: CreateUser):
    hashed_password = get_password_hash(user.password)

    existing_user = await get_user_by_username(db, user.username)
    if existing_user:
        raise UserAlreadyExistsException()

    user = User(username=user.username, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    return user

# Поиск пользователя по имени
async def get_user_by_username(db: AsyncSession, username: str):
    return (await db.execute(select(User).where(User.username == username))).scalar()

# Аутентификация пользователя
async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    logger.info(f"Logging in user with username: {user}")
    if not user:
        raise IncorrectCredentialsException()
    if not verify_password(password, user.hashed_password):
        raise ValidateCredentialsException()

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return Token(access_token=access_token)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Функция для получения текущего пользователя по токену
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    payload = decode_access_token(token)
    if payload is None:
        raise ValidateCredentialsException()
    username = payload.get("sub")
    if username is None:
        raise ValidateCredentialsException()
    user = await get_user_by_username(db, username)
    if user is None:
        raise ValidateCredentialsException()
    return user