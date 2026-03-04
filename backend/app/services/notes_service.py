from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select

from app.ai import OllamaClient, select_model
from app.schemas.notes import NotesGenerateRequest, NotesResponse
from app.models.notes import GeneratedNote
from app.models.user import User
from app.security.guards import enforce_client_capabilities

ollama = OllamaClient()


LATEX_SAFE_NOTES_PROMPT = """
You are an expert textbook author writing high-quality academic notes.

TASK:
Generate clear, structured, textbook-quality study notes that are detailed in content and context.

SUBJECT: {subject}
CHAPTER: {chapter}
DIFFICULTY: {difficulty}

MANDATORY FORMATTING RULES (STRICT):
1. ALL mathematical expressions MUST use valid LaTeX.
2. Inline math MUST use: \\( ... \\)
3. Display math MUST use:
   \\[
   ...
   \\]
4. DO NOT use $ or $$.
5. Ensure full KaTeX compatibility.

CONTENT STRUCTURE:
- Proper headings
- Bullet points
- Worked examples
- Exam-focused clarity
- No hallucinations
"""


async def generate_student_notes(
    payload: NotesGenerateRequest,
    db: AsyncSession,
    current_user: User,
) -> NotesResponse:

    # 1️⃣ Enforce model access rules
    enforce_client_capabilities(payload.context)

    # 2️⃣ Select model
    model = select_model(payload.context)

    # 3️⃣ Build prompt
    prompt = LATEX_SAFE_NOTES_PROMPT.format(
        subject=payload.subject,
        chapter=payload.chapter,
        difficulty=payload.difficulty,
    )

    # 4️⃣ Generate content from Ollama
    raw_content = await ollama.generate(
        prompt=prompt,
        model_name=model,
        temperature=0.3,
        max_tokens=20000 if payload.context.client_type == "desktop" else 18000,
    )

    if not raw_content or not raw_content.strip():
        raise HTTPException(status_code=400, detail="AI returned empty content")

    # 5️⃣ Store in DB
    note = GeneratedNote(
        user_id=current_user.id,
        subject=payload.subject,
        chapter=payload.chapter,
        difficulty=payload.difficulty,
        content=raw_content,  # KaTeX-safe markdown
        is_student_generated=True,
        is_teacher_provided=False,
        is_saved=False,
        is_synced=False,
    )

    db.add(note)
    await db.commit()
    await db.refresh(note)

    # 6️⃣ Return structured response
    return NotesResponse(
        content_id=str(note.id),
        summary=f"{payload.chapter} notes generated successfully.",
        pdf_url=None,
        offline_ready=True,
        expires_at=None,
    )
