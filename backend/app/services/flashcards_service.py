import json
from typing import Any, Dict, List

from app.ai import OllamaClient, select_model
from app.schemas.flashcards import FlashcardSetResponse
from app.schemas.common import ClientContext

ollama = OllamaClient()


async def generate_flashcards(
    subject: str,
    chapter: str,
    context: ClientContext,
) -> FlashcardSetResponse:
    model = select_model(context)

    prompt = f"""
Generate high-quality flashcards.

Subject: {subject}
Chapter: {chapter}

Rules:
- Short
- Fact-based
- Exam-focused
- Output as JSON array of objects with keys "front" and "back"
"""

    response = await ollama.generate(
        prompt=prompt,
        model_name=model,
        temperature=0.3,
        max_tokens=800,
    )

    cards = _parse_cards(response)

    return FlashcardSetResponse(
        set_id=0,
        subject=subject,
        chapter=chapter,
        cards=cards,
    )


def _parse_cards(response: str) -> List[Dict[str, str]]:
    cleaned = response.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

    parsed_cards = _parse_json_cards(cleaned)
    if parsed_cards:
        return parsed_cards

    cards: List[Dict[str, str]] = []
    pending_front: str | None = None

    for raw_line in response.splitlines():
        line = raw_line.strip(" -*\t")
        if " - " in line:
            front, back = line.split(" - ", 1)
        else:
            if ":" not in line:
                continue

            key, value = line.split(":", 1)
            normalized_key = key.strip().strip("\"'").lower()
            value = value.strip()

            if normalized_key in {"front", "question", "q", "prompt", "term"}:
                pending_front = value or None
                continue

            if normalized_key in {"back", "answer", "a", "definition", "explanation"}:
                if pending_front and value:
                    cards.append({"front": pending_front, "back": value})
                    pending_front = None
                continue

            continue

        front = front.strip()
        back = back.strip()
        if front and back:
            cards.append({"front": front, "back": back})

    if not cards:
        raise ValueError("AI did not return parseable flashcards")

    return cards[:20]


def _parse_json_cards(cleaned: str) -> List[Dict[str, str]]:
    try:
        parsed: Any = json.loads(cleaned)
    except Exception:
        return []

    raw_cards: Any = parsed
    if isinstance(parsed, dict):
        raw_cards = parsed.get("cards") or parsed.get("flashcards")

    if not isinstance(raw_cards, list):
        return []

    cards: List[Dict[str, str]] = []
    for card in raw_cards:
        if not isinstance(card, dict):
            continue
        front = str(
            card.get("front")
            or card.get("question")
            or card.get("q")
            or card.get("prompt")
            or card.get("term")
            or ""
        ).strip()
        back = str(
            card.get("back")
            or card.get("answer")
            or card.get("a")
            or card.get("definition")
            or card.get("explanation")
            or ""
        ).strip()
        if front and back:
            cards.append({"front": front, "back": back})

    return cards[:20]
