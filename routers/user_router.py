__all__ = ["user_router"]
from fastapi import Depends, APIRouter
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
from database.init_database import get_db
from CRUD.users import create_user, authenticate_user
from schemas.user import CreateUser
from logger import log_error, log_user_action

user_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

rate_limiter = RateLimiter(times=5, seconds=10)

@user_router.post("/register/", dependencies=[Depends(rate_limiter)])
async def register(user: CreateUser, db: AsyncSession = Depends(get_db)):
    log_user_action(user.username, f"Made request to register")
    return await create_user(db, user)

# Маршрут для логина (аутентификация)
@user_router.post("/login/", dependencies=[Depends(rate_limiter)])
async def login(user: CreateUser, db: AsyncSession = Depends(get_db)):
    log_user_action(user.username, f"Made request to login")
    return await authenticate_user(db, user.username, user.password)
