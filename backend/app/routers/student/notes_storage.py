from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO
from playwright.async_api import async_playwright
import markdown

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.notes import GeneratedNote
from app.routers.student._guards import student_guard
from fastapi.responses import PlainTextResponse
from app.security import get_current_user
from app.models.user import User
from app.models.notes import GeneratedNote




router = APIRouter(
    prefix="/api/student/notes/storage",
    tags=["Student Notes Storage"],
    dependencies=[student_guard],
)


@router.post("/{note_id}/save")
async def save_note(note_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(GeneratedNote).where(GeneratedNote.id == note_id)
    )
    note = result.scalar_one_or_none()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.is_saved = True
    await db.commit()

    return {"status": "saved"}


@router.get("/")
async def list_saved_notes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(GeneratedNote).where(GeneratedNote.is_saved == True)
    )
    notes = result.scalars().all()

    return [
        {
            "id": n.id,
            "subject": n.subject,
            "chapter": n.chapter,
            "created_at": n.created_at,
            "offline_ready": n.is_synced,
        }
        for n in notes
    ]


@router.get("/{note_id}")
async def get_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(GeneratedNote).where(GeneratedNote.id == note_id)
    )

    note = result.scalar_one_or_none()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.is_student_generated and note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return {
        "id": note.id,
        "subject": note.subject,
        "chapter": note.chapter,
        "content": note.content,  # KaTeX-safe
    }


'''@router.get("/{note_id}/download")
async def download_note(note_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(GeneratedNote).where(GeneratedNote.id == note_id)
    )
    note = result.scalar_one_or_none()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return PlainTextResponse(
        note.extra_data["content"],
        media_type="text/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="notes_{note_id}.pdf"'
        },
    )
'''

@router.get("/{note_id}/pdf")
async def generate_note_pdf(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(GeneratedNote).where(
            GeneratedNote.id == note_id,
            GeneratedNote.user_id == current_user.id,
        )
    )
    note = result.scalar_one_or_none()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if not note.content:
        raise HTTPException(status_code=400, detail="No content available")

    html_body = markdown.markdown(
        note.content,
        extensions=["fenced_code", "tables"]
    )

    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">

        <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">

        <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>

        <style>
            body {{
                font-family: Arial, sans-serif;
                padding: 40px;
                line-height: 1.6;
            }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.set_content(full_html, wait_until="networkidle")

        # Wait for KaTeX to be available
        await page.wait_for_function("window.katex !== undefined")

        # Manually trigger rendering
        await page.evaluate("""
            renderMathInElement(document.body, {
                delimiters: [
                    {left: "\\\\(", right: "\\\\)", display: false},
                    {left: "\\\\[", right: "\\\\]", display: true}
                ]
            });
        """)

        # Small delay to allow layout
        await page.wait_for_timeout(300)

        pdf_bytes = await page.pdf(
            format="A4",
            print_background=True,
        )

        await browser.close()

    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"inline; filename=note_{note_id}.pdf"
        },
    )