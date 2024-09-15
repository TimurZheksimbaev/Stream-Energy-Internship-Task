__all__ = ["notes_router"]

from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
from database.init_database import get_db
from models.models import User
from CRUD.notes import create_note, update_note, get_notes, delete_note_by_id, get_notes_by_tags, get_notes_by_title
from schemas.note import CreateNote, SearchByTags
from CRUD.users import get_current_user
from logger import log_user_action, log_error

notes_router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)

rate_limiter = RateLimiter(times=5, seconds=10)

@notes_router.post("/create/", dependencies=[Depends(rate_limiter)])
async def create_new_note(newNote: CreateNote, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    note = await create_note(db, newNote, user)
    log_user_action(user.username, f"Made request to create note")
    return note

@notes_router.put("/update/{note_id}", dependencies=[Depends(rate_limiter)])
async def update_note(note_id: int, new_note: CreateNote, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    log_user_action(user.username, f"Made request to update note with id {note_id}")
    return await update_note(db, note_id, new_note, user)

@notes_router.get("/list/", dependencies=[Depends(rate_limiter)])
async def read_notes(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    log_user_action(user.username, f"Made request to get notes")
    return await get_notes(db, user)

@notes_router.delete("/delete/{note_id}", dependencies=[Depends(rate_limiter)])
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    log_user_action(user.username, f"Made request to delete note with id {note_id}")
    await delete_note_by_id(db, note_id, user)

@notes_router.get("/search_by_tags/", dependencies=[Depends(rate_limiter)])
async def search_notes_by_tags(tags: SearchByTags, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    log_user_action(user.username, f"Made request to search notes by tags")
    return await get_notes_by_tags(db, tags, user)

@notes_router.get("/search_by_title/", dependencies=[Depends(rate_limiter)])
async def search_notes_by_title(title: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    log_user_action(user.username, f"Made request to search notes by title")
    return await get_notes_by_title(db, title, user)