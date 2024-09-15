from typing import List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Note, User
from schemas.note import CreateNote, SearchByTags
from exceptions import NoNoteException, NoNoteForSuchTagsException, NoNoteWithSuchTitleException
from logger import log_user_action, log_error

async def create_note(db: AsyncSession, note: CreateNote, user: User) -> Note:
    note = Note(title=note.title, content=note.content, owner_id=user.id, tags=note.tags)
    db.add(note)
    await db.commit()
    log_user_action(user.username, f"Created note: {note.title}")
    return note

async def update_note(db: AsyncSession, note_id: int, newNote: CreateNote, user: User):
    note = await get_note_by_id(db, note_id, user.id)
    if note is None or note.owner_id != user.id:
        log_error(f"User with id {user.username} tried to update note with id {note_id}")
        raise NoNoteException()

    if newNote.title:
        note.title = newNote.title
    if newNote.content:
        note.content = newNote.content
    if newNote.tags is not None:
        note.tags = newNote.tags

    await db.commit()
    await db.refresh(note)
    log_user_action(user.username, f"Updated note: {note.title}")
    return note


async def get_notes(db: AsyncSession, user: User) -> List[Note]:
    notes = (await db.execute(select(Note).where(Note.owner_id == user.id))).scalars().all()
    if not notes:
        log_error(f"User {user.username} tried to get notes")
        raise NoNoteException()
    log_user_action(user.username, f"Got notes")
    return notes

async def get_note_by_id(db: AsyncSession, note_id: int, user: User) -> Note:
    note = (await db.execute(select(Note).where(Note.id == note_id, Note.owner_id == user.id))).scalar()
    if not note:
        log_error(f"User {user.username} tried to get note with id {note_id}")
        raise NoNoteException()
    log_user_action(user.username, f"Got note with id {note_id}")
    return note

async def delete_note_by_id(db: AsyncSession, note_id: int, user: User):
    note = await get_note_by_id(db, note_id, user.id)
    if note:
        await db.delete(note)
        await db.commit()
        log_user_action(user.username, f"Deleted note with id {note_id}")
    else:
        log_error(f"User {user.username} tried to delete note with id {note_id}")
        raise NoNoteException()

async def get_notes_by_tags(db: AsyncSession, tags: SearchByTags, user: User) -> List[Note]:
    query = select(Note).where(Note.owner_id == user.id)
    if tags:
        query = query.where(Note.tags.overlap(tags.tags))
    notes = (await db.execute(query)).scalars().all()
    if not notes:
        log_error(f"User {user.username} tried to get notes with tags {tags.tags}")
        raise NoNoteForSuchTagsException()
    log_user_action(user.username, f"Got notes with tags {tags.tags}")
    return notes


async def get_notes_by_title(db: AsyncSession, title: str, user: User) -> List[Note]:
    new_query = select(Note).where(Note.title.like(title)).where(Note.owner_id == user.id)
    notes = (await db.execute(new_query)).scalars().all()
    if not notes:
        log_error(f"User {user.username} tried to get notes with title {title}")
        raise NoNoteWithSuchTitleException()
    log_user_action(user.username, f"Got notes with title {title}")
    return notes
