from typing import List
from datetime import datetime
from app.schemas.sync import SyncItem, SyncResponse
from sqlalchemy import select
from app.models.notes import GeneratedNote
from sqlalchemy.ext.asyncio import AsyncSession


async def get_available_sync_items(
    last_sync_at: str | None,
    client_known_ids: List[str],
    db: AsyncSession
) -> SyncResponse:
    """
    Returns only content that is new or updated since last sync.
    """

    # Placeholder canonical content registry
    items = []

    result = await db.execute(select(GeneratedNote))
    notes = result.scalars().all()
    
    for note in notes.scalars():
        if str(note.id) not in client_known_ids:
            items.append({
                "content_id": str(note.id),
                "content_type": "notes",
                "version": "v1",
                "updated_at": note.created_at.isoformat(),
            })
            note.is_synced = True

    await db.commit()
    return {"available": items}

