from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.progress import Progress
import time


# XP rules (authoritative, backend-only)
XP_RULES = {
    "TEST_COMPLETED": 100,
    "ASSIGNMENT_SUBMITTED": 75,
    "NOTES_GENERATED": 40,
    "FLASHCARDS_REVIEWED": 30,
    "AI_CHAT_INTERACTION": 10,
    "DAILY_STREAK_BONUS": 50,
}

XP_COOLDOWNS = {
    "TEST_COMPLETED": 0,            # XP handled by score logic elsewhere
    "ASSIGNMENT_SUBMITTED": 3 * 60 * 60,   # 3 hours
    "NOTES_GENERATED":  60 * 60,       # 1 hour
    "FLASHCARDS_REVIEWED": 30 * 60,    # 30 minutes
    "AI_CHAT_INTERACTION": 30 * 60,        # 30 minutes
    "DAILY_STREAK_BONUS": 24 * 60 * 60,    # 24 hours
}


def calculate_level(xp: int) -> int:
    """
    Simple level curve:
    Level increases every 500 XP.
    """
    return max(1, xp // 500 + 1)


async def apply_xp_event(
    db: AsyncSession,
    user_id: int,
    event: str,
) -> Progress:
    """
    Applies XP for a given event with cooldown enforcement.
    """

    xp_gain = XP_RULES.get(event)
    if xp_gain is None:
        raise ValueError(f"Unknown XP event: {event}")

    cooldown = XP_COOLDOWNS.get(event, 0)
    now = int(time.time())

    result = await db.execute(
        select(Progress).where(Progress.user_id == user_id)
    )
    progress = result.scalar_one_or_none()

    if progress is None:
        progress = Progress(
            user_id=user_id,
            xp=0,
            level=1,
            stats={},
        )
        db.add(progress)
        await db.flush()

    # Ensure stats dict exists
    stats = progress.stats or {}
    last_event_time = stats.get(event)

    # Cooldown check
    if last_event_time is not None and cooldown > 0:
        if now - last_event_time < cooldown:
            # Cooldown active → no XP awarded
            return progress

    # Apply XP
    progress.xp += xp_gain
    progress.level = calculate_level(progress.xp)

    # Update event timestamp
    stats[event] = now
    progress.stats = stats

    await db.commit()
    await db.refresh(progress)

    return progress

