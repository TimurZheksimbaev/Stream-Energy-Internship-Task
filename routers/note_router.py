__all__ = ["notes_router"]

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.init_database import get_db
from models.models import User
from CRUD.notes import create_note, update_note, get_notes, delete_note_by_id, get_notes_by_tags, get_notes_by_title
from schemas.note import CreateNote, SearchByTags
from CRUD.users import get_current_user
from loggers.logger import logger


notes_router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)

@notes_router.post("/create/")
async def create_new_note(newNote: CreateNote, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    note = await create_note(db, newNote, user.id)
    return note

@notes_router.put("/update/{note_id}")
async def update_note(note_id: int, new_note: CreateNote, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await update_note(db, note_id, new_note, user.id)

@notes_router.get("/list/")
async def read_notes(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await get_notes(db, user.id)

@notes_router.delete("/delete/{note_id}")
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    await delete_note_by_id(db, note_id, user.id)

@notes_router.get("/search/tag/")
async def search_notes_by_tags(tags: SearchByTags, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await get_notes_by_tags(db, tags, user.id)

@notes_router.get("/search/title/")
async def search_notes_by_title(title: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await get_notes_by_title(db, title, user.id)