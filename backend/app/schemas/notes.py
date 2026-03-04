from pydantic import BaseModel
from typing import Optional
from app.schemas.common import ClientContext


class NotesGenerateRequest(BaseModel):
    subject: str
    chapter: str
    difficulty: str
    context: ClientContext


class NotesResponse(BaseModel):
    content_id: str
    summary: str
    pdf_url: Optional[str] = None
    offline_ready: bool
    expires_at: Optional[str] = None