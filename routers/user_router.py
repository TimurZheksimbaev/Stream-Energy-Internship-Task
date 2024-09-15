__all__ = ["user_router"]

from typing import Dict

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database.init_database import get_db
from CRUD.users import create_user, authenticate_user, get_user_by_username
from schemas.user import CreateUser
from loggers.logger import logger


user_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@user_router.post("/register/")
async def register(user: CreateUser, db: AsyncSession = Depends(get_db)):
    logger.info(f"Registering new user with username: {user.username}")
    return await create_user(db, user)

# Маршрут для логина (аутентификация)
@user_router.post("/login/")
async def login(user: CreateUser, db: AsyncSession = Depends(get_db)):
    logger.info(f"Logging in user with username: {user.password}")
    return await authenticate_user(db, user.username, user.password)
