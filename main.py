from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from database.init_database import engine, Base
from routers.note_router import notes_router
from routers.user_router import user_router

# create app
app = FastAPI()

# add routers
app.include_router(notes_router)
app.include_router(user_router)

@app.on_event("startup")
async def startup():
    redis_connection = redis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_connection)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)