from typing import List

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Note
from schemas.note import CreateNote, SearchByTags
from exceptions import NoNoteException, NoNoteForSuchTagsException, NoNoteWithSuchTitleException

async def create_note(db: AsyncSession, note: CreateNote, owner_id: int) -> Note:
    note = Note(title=note.title, content=note.content, owner_id=owner_id, tags=note.tags)
    db.add(note)
    await db.commit()
    return note

async def update_note(db: AsyncSession, note_id: int, newNote: CreateNote, user_id: int):
    note = await get_note_by_id(db, note_id, user_id)
    if note is None or note.owner_id != user_id:
        raise NoNoteException()

    # Обновляем поля только если они были переданы
    if newNote.title:
        note.title = newNote.title
    if newNote.content:
        note.content = newNote.content
    if newNote.tags is not None:
        note.tags = newNote.tags

    await db.commit()
    await db.refresh(note)
    return note


async def get_notes(db: AsyncSession, user_id: int) -> List[Note]:
    notes = (await db.execute(select(Note).where(Note.owner_id == user_id))).scalars().all()
    if not notes:
        raise NoNoteException()
    return notes
async def get_note_by_id(db: AsyncSession, note_id: int, user_id: int) -> Note:
    note = (await db.execute(select(Note).where(Note.id == note_id, Note.owner_id == user_id))).scalar()
    if not note:
        raise NoNoteException()
    return note
async def delete_note_by_id(db: AsyncSession, note_id: int, user_id: int):
    note = await get_note_by_id(db, note_id, user_id)
    if note:
        await db.delete(note)
        await db.commit()
    else:
        raise NoNoteException()

async def get_notes_by_tags(db: AsyncSession, tags: SearchByTags, user_id: int) -> List[Note]:
    query = select(Note).where(Note.owner_id == user_id)
    if tags:
        query = query.where(Note.tags.overlap(tags.tags))
    notes = (await db.execute(query)).scalars().all()
    if not notes:
        raise NoNoteForSuchTagsException()
    return notes


async def get_notes_by_title(db: AsyncSession, title: str, user_id: int) -> List[Note]:
    # query = select(Note).where(Note.owner_id == user_id)

    new_query = select(Note).where(Note.title.like(title).where(Note.owner_id == user_id))

    notes = (await db.execute(new_query)).scalars().all()
    if not notes:
        raise NoNoteWithSuchTitleException()
    return notes
