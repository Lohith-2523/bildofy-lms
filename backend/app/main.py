from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.logging.middleware import logging_middleware
from app.middleware.audit import AuditMiddleware

# 🔹 Routers
from app.routers import auth
from app.routers import subjects
from app.routers import teacher_tests
from app.routers import analytics_export
from app.routers import analytics

from app.routers.student import (
    notes_router,
    flashcards_router,
    tests_router,
    ai_chat_router,
    progress_router,
    sync_router,
    teacher_notes_router,
    subjects as student_subjects,
    notes_storage
)

from app.routers.teacher import (
    assignments_router,
    tests_router as teacher_tests_router,
    ai_tools_router,
    reports_router,
    students as teacher_students,
)

from app.routers.parent import (
    overview_router as parent_overview_router,
    progress_router as parent_progress_router,
    insights_router as parent_insights_router,
)

from app.routers.admin import (
    users_router as admin_users_router,
    content_router as admin_content_router,
    system_router as admin_system_router,
)



# -------------------------------------------------------------------

settings = get_settings()

# ✅ CREATE FASTAPI APP
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)

# -------------------------------------------------------------------
# 🔹 Middleware
# -------------------------------------------------------------------

app.middleware("http")(logging_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuditMiddleware)


# -------------------------------------------------------------------
# 🔹 Routers
# -------------------------------------------------------------------

# Auth
app.include_router(auth.router)

# Subjects (admin-only)
app.include_router(subjects.router)

# Student routers
app.include_router(notes_router)
app.include_router(flashcards_router)
app.include_router(tests_router)
app.include_router(ai_chat_router)
app.include_router(progress_router)
app.include_router(sync_router)
app.include_router(teacher_notes_router)
app.include_router(student_subjects.router)

app.include_router(analytics.router)
app.include_router(analytics_export.router)
app.include_router(notes_storage.router)

# Teacher routers
app.include_router(assignments_router)
app.include_router(teacher_tests_router)
app.include_router(ai_tools_router)
app.include_router(reports_router)
app.include_router(teacher_students.router)

# Parent routers
app.include_router(parent_overview_router)
app.include_router(parent_progress_router)
app.include_router(parent_insights_router)

# Admin routers
app.include_router(admin_users_router)
app.include_router(admin_content_router)
app.include_router(admin_system_router)
app.include_router(teacher_tests.router)

# -------------------------------------------------------------------
# 🔹 Health & Meta
# -------------------------------------------------------------------

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/version")
async def version():
    return {
        "app": settings.APP_NAME,
        "env": settings.APP_ENV,
    }
