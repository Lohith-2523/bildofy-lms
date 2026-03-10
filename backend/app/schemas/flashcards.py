from pydantic import BaseModel
from typing import List

from app.schemas.common import ClientContext


class Flashcard(BaseModel):
    front: str
    back: str


class FlashcardSetResponse(BaseModel):
    set_id: int
    subject: str
    chapter: str
    cards: List[Flashcard]


class FlashcardsGenerateRequest(BaseModel):
    subject: str
    chapter: str
    context: ClientContext
