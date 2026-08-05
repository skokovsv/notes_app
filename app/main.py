from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import engine, Base, get_session
from app.models import Note
from app.schemas import NoteCreate, NoteOut

app = FastAPI(title="Notes API")


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/notes", response_model=NoteOut, status_code=201)
async def create_note(note: NoteCreate, session: AsyncSession = Depends(get_session)):
    db_note = Note(title=note.title, content=note.content)
    session.add(db_note)
    await session.commit()
    await session.refresh(db_note)
    return db_note


@app.get("/notes", response_model=list[NoteOut])
async def list_notes(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Note).order_by(Note.created_at.desc()))
    return result.scalars().all()


@app.get("/notes/{note_id}", response_model=NoteOut)
async def get_note(note_id: str, session: AsyncSession = Depends(get_session)):
    note = await session.get(Note, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.delete("/notes/{note_id}", status_code=204)
async def delete_note(note_id: str, session: AsyncSession = Depends(get_session)):
    note = await session.get(Note, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    await session.delete(note)
    await session.commit()
