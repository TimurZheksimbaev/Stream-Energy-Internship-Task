import asyncio
from fastapi import FastAPI
from database.init_database import engine, Base
from routers.note_router import notes_router
from routers.user_router import user_router
from loggers.logger import logger
# create app
app = FastAPI()

# add routers
app.include_router(notes_router)
app.include_router(user_router)
# Base.metadata.create_all(bind=engine)

# async def init_models():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#
# asyncio.run(init_models())

@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)