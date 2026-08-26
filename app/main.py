from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import engine, Base, get_session
from app.models import Note
from app.schemas import NoteCreate, NoteOut, NoteListResponse
from app.security import verify_api_key


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Notes API", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/notes", response_model=NoteOut, status_code=201, dependencies=[Depends(verify_api_key)])
async def create_note(note: NoteCreate, session: AsyncSession = Depends(get_session)):
    db_note = Note(title=note.title, content=note.content)
    session.add(db_note)
    await session.commit()
    await session.refresh(db_note)
    return db_note


@app.get("/notes", response_model=NoteListResponse)
async def list_notes(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
):
    total = (await session.execute(select(func.count()).select_from(Note))).scalar_one()

    result = await session.execute(
        select(Note)
        .order_by(Note.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    notes = result.scalars().all()

    return NoteListResponse(items=notes, total=total, page=page, page_size=page_size)


@app.get("/notes/{note_id}", response_model=NoteOut)
async def get_note(note_id: str, session: AsyncSession = Depends(get_session)):
    note = await session.get(Note, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.delete("/notes/{note_id}", status_code=204, dependencies=[Depends(verify_api_key)])
async def delete_note(note_id: str, session: AsyncSession = Depends(get_session)):
    note = await session.get(Note, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    await session.delete(note)
    await session.commit()