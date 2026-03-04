from ..models.flashcards import FlashcardSet
from .base_repo import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession
import json


class FlashcardRepo(BaseRepo[FlashcardSet]):
    def __init__(self):
        super().__init__(FlashcardSet)

    async def create_set(self, db: AsyncSession, user_id: int, title: str, subject: str, cards: list):
        obj = FlashcardSet(user_id=user_id, title=title, subject=subject, metadata=json.dumps(cards, ensure_ascii=False))
        return await self.create(db, obj)
