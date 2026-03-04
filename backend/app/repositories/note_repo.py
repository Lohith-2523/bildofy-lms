from ..models.notes import GeneratedNote
from .base_repo import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession


class NoteRepo(BaseRepo[GeneratedNote]):
    def __init__(self):
        super().__init__(GeneratedNote)

    async def create_note(self, db: AsyncSession, **kwargs):
        n = GeneratedNote(**kwargs)
        return await self.create(db, n)
