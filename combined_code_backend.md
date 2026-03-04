# Combined Project Code


---

### `backend\app\config.py`

```python
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    # App
    APP_NAME: str = "AI LMS Backend"
    APP_ENV: Literal["local", "staging", "production"] = "local"
    DEBUG: bool = False

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_TIMEOUT_SECONDS: int = 120

    # Model routing
    OFFLINE_MODEL_NAME: str = "phi3:mini"
    ONLINE_MODEL_NAME: str = "mistral:7b-instruct"

    # Payload limits
    MAX_RESPONSE_KB_MOBILE: int = 256
    MAX_RESPONSE_KB_DESKTOP: int = 1024

    # Database
    DATABASE_URL: str

    # Logging
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    # ✅ THIS IS THE IMPORTANT PART
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",   # <-- ignore unknown env vars
    )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7



@lru_cache
def get_settings() -> Settings:
    return Settings()

```

---

### `backend\app\loop_fix.py`

```python
import asyncio
import sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

```

---

### `backend\app\main.py`

```python
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

```

---

### `backend\app\__init__.py`

```python

```

---

### `backend\app\ai\__init__.py`

```python
from app.ai.ollama_client import OllamaClient
from app.ai.model_router import select_model

```

---

### `backend\app\logging\__init__.py`

```python
from app.logging.logger import logger
from app.logging.middleware import logging_middleware

```

---

### `backend\app\models\__init__.py`

```python
from app.models.assignments import Assignment
from app.models.flashcards import FlashcardSet
from app.models.progress import Progress

```

---

### `backend\app\rag\__init__.py`

```python
from app.rag.context_builder import build_context
from app.rag.retriever import VectorRetriever
from app.rag.guardrails import validate_context

```

---

### `backend\app\routers\admin\__init__.py`

```python
from app.routers.admin.users import router as users_router
from app.routers.admin.content import router as content_router
from app.routers.admin.system import router as system_router

```

---

### `backend\app\routers\parent\__init__.py`

```python
from app.routers.parent.overview import router as overview_router
from app.routers.parent.progress import router as progress_router
from app.routers.parent.insights import router as insights_router

```

---

### `backend\app\routers\student\__init__.py`

```python
from app.routers.student.notes import router as notes_router
from app.routers.student.flashcards import router as flashcards_router
from app.routers.student.tests import router as tests_router
from app.routers.student.ai_chat import router as ai_chat_router
from app.routers.student.progress import router as progress_router
from app.routers.student.sync import router as sync_router
from app.routers.student.teacher_notes import router as teacher_notes_router

```

---

### `backend\app\routers\teacher\__init__.py`

```python
from app.routers.teacher.assignments import router as assignments_router
from app.routers.teacher.tests import router as tests_router
from app.routers.teacher.ai_tools import router as ai_tools_router
from app.routers.teacher.reports import router as reports_router
from app.routers.teacher.notes import router as notes_router

```

---

### `backend\app\schemas\__init__.py`

```python
from app.schemas.common import ClientContext
from app.schemas.user import UserResponse
from app.schemas.notes import NotesGenerateRequest, NotesResponse
from app.schemas.tests import TestCreateRequest, TestResponse
from app.schemas.assignments import AssignmentCreateRequest, AssignmentResponse
from app.schemas.flashcards import FlashcardSetResponse
from app.schemas.progress import ProgressResponse

```

---

### `backend\app\security\__init__.py`

```python
from app.security.guards import enforce_client_capabilities
from app.security.rate_limiter import rate_limit
from app.security.admin_guard import require_admin
from app.security.roles import Role
from app.security.dependencies import get_current_user, require_role

```

---

### `backend\app\services\__init__.py`

```python
from app.services.notes_service import generate_student_notes
from app.services.flashcards_service import generate_flashcards
from app.services.test_service import generate_test
from app.services.ai_service import chat_with_ai
from app.services.xp_service import apply_xp_event

from app.services.teacher_assignment_service import create_assignment
from app.services.teacher_test_service import (
    create_test_manual,
    create_test_ai_assisted,
)
from app.services.teacher_ai_service import (
    suggest_test_questions,
    suggest_assignment_outline,
)
from app.services.teacher_report_service import get_student_report

from app.services.parent_overview_service import (
    get_parent_overview,
    get_detailed_progress,
)
from app.services.parent_insights_service import get_parent_insights

from app.services.admin_user_service import (
    list_users,
    get_user,
    update_user_role,
    disable_user,
)
from app.services.admin_system_service import get_system_status
from app.services.teacher_notes_service import (
    create_manual_notes,
    generate_teacher_notes,
    upload_notes_file,
)
from app.services.file_validation import validate_upload

```

---

### `backend\app\ai\model_router.py`

```python
from app.schemas.common import ClientContext
from app.config import get_settings

settings = get_settings()


def select_model(context: ClientContext) -> str:
    """
    Determines which model to use based on client capabilities.
    """

    # Offline or light-capability clients always use the lightweight model
    if context.connectivity == "offline" or context.model_capability == "light":
        return settings.OFFLINE_MODEL_NAME

    # Online + heavy-capability clients use the server-grade model
    return settings.ONLINE_MODEL_NAME

```

---

### `backend\app\ai\ollama_client.py`

```python
import httpx
from typing import Dict, Any
from app.config import get_settings

settings = get_settings()


class OllamaClient:
    def __init__(self) -> None:
        self.base_url = settings.OLLAMA_BASE_URL
        self.timeout = settings.OLLAMA_TIMEOUT_SECONDS

    async def _post(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json=payload,
            )
            response.raise_for_status()
            return response.json()

    async def generate(
        self,
        prompt: str,
        model_name: str,
        temperature: float = 0.3,
        max_tokens: int = 1024,
    ) -> str:
        payload = {
            "model": model_name,
            "prompt": prompt,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
            "stream": False,
        }

        result = await self._post(payload)
        return result.get("response", "").strip()

```

---

### `backend\app\db\base.py`

```python
from app.db.session import Base

# existing imports
from app.models.user import User
from app.models.subject import Subject
from app.models.classroom import Classroom
from app.models.progress import Progress
# WC-2 imports
from app.models.test import Test
from app.models.test_question import TestQuestion
from app.models.test_attempt import TestAttempt
from app.models.test_answer import TestAnswer
from app.models.audit_log import AuditLog
from app.models.notes import GeneratedNote
from app.models.subject_student import SubjectStudent

__all__ = [
    "Base",
    "User",
    "Subject",
    "Test",
    "GeneratedNote",
    "AuditLog",
]
```

---

### `backend\app\db\base_imports.py`

```python
# Import all models here so Base.metadata knows about them\
from app.models.user import User
from app.models.progress import Progress
from app.models.classroom import Classroom
# add others as needed
from app.models.subject import Subject
from app.models.subject_student import SubjectStudent



```

---

### `backend\app\db\init_db.py`

```python
import asyncio
from app.db.session import engine
from app.db.session import Base
import app.db.base_imports  # IMPORTANT

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_models())

```

---

### `backend\app\db\session.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    future=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

```

---

### `backend\app\logging\logger.py`

```python
from loguru import logger
import sys

logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level}</level> | "
           "{message}",
)

```

---

### `backend\app\logging\middleware.py`

```python
from fastapi import Request
from app.logging.logger import logger
import time


async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = int((time.time() - start_time) * 1000)

    logger.info(
        f"{request.method} {request.url.path} "
        f"{response.status_code} {duration}ms"
    )

    return response

```

---

### `backend\app\middleware\audit.py`

```python
from starlette.middleware.base import BaseHTTPMiddleware
from app.db.session import AsyncSessionLocal
from app.models.audit_log import AuditLog


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        user_id = getattr(request.state, "user_id", None)

        async with AsyncSessionLocal() as db:
            db.add(
                AuditLog(
                    user_id=user_id,
                    action=request.method,
                    endpoint=request.url.path,
                )
            )
            await db.commit()

        return response

```

---

### `backend\app\models\assignments.py`

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.db.session import Base


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    subject = Column(String(100), nullable=False)

    due_date = Column(DateTime(timezone=True), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

```

---

### `backend\app\routers\student\assignments.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ...db.session import get_db
from ...repositories.assignment_repo import AssignmentRepo
from ...schemas.assignments import AssignmentOut
from app.routers.student._guards import student_guard

router = APIRouter(prefix="/api/student/assignments", tags=["student.assignments"], dependencies=[student_guard])
repo = AssignmentRepo()


@router.get("/", response_model=list[AssignmentOut])
async def list_assignments(db: AsyncSession = Depends(get_db)):
    rows = await repo.list(db)
    return rows

```

---

### `backend\app\routers\teacher\assignments.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal

from app.db.session import get_db
from app.schemas.assignments import AssignmentCreateRequest, AssignmentResponse
from app.services.teacher_assignment_service import create_assignment
from app.routers.teacher._guards import teacher_guard

router = APIRouter(prefix="/api/teacher/assignments", tags=["Teacher Assignments"])


@router.post("/create", response_model=AssignmentResponse)
async def create_assignment_endpoint(
    payload: AssignmentCreateRequest,
    assignment_type: Literal["LMS_ATTEMPT", "PDF_UPLOAD"],
    db: AsyncSession = Depends(get_db),
):
    """
    assignment_type:
    - LMS_ATTEMPT → student answers inside LMS
    - PDF_UPLOAD → student uploads a PDF
    """
    return await create_assignment(payload, assignment_type, db)

```

---

### `backend\app\schemas\assignments.py`

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Literal, Optional


class AssignmentCreateRequest(BaseModel):
    title: str
    subject: str
    description: Optional[str] = None
    due_date: datetime


class AssignmentResponse(BaseModel):
    id: int
    title: str
    subject: str
    due_date: datetime

```

---

### `backend\app\models\audit_log.py`

```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.session import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    action = Column(String, nullable=False)
    endpoint = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

```

---

### `backend\app\models\classroom.py`

```python
from sqlalchemy import Column, Integer, String
from app.db.session import Base


class Classroom(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    grade = Column(Integer, nullable=False)
    section = Column(String, nullable=False)  # A, B, C
    code_prefix = Column(String, unique=True, nullable=False)  # e.g. "1103"

```

---

### `backend\app\models\flashcards.py`

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.session import Base


class FlashcardSet(Base):
    __tablename__ = "flashcard_sets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    subject = Column(String(100), nullable=False)
    chapter = Column(String(200), nullable=False)

    cards = Column(JSON, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

```

---

### `backend\app\routers\student\flashcards.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.common import ClientContext
from app.services.flashcards_service import generate_flashcards
from app.services.xp_service import apply_xp_event
from app.routers.student._guards import student_guard

router = APIRouter(prefix="/api/student/flashcards", tags=["Student Flashcards"], dependencies=[student_guard])


@router.post("/generate")
async def generate_flashcards_endpoint(
    subject: str,
    chapter: str,
    context: ClientContext,
    db: AsyncSession = Depends(get_db),
):
    response = await generate_flashcards(subject, chapter, context)
    await apply_xp_event(db, user_id=1, event="FLASHCARDS_REVIEWED")
    return response

```

---

### `backend\app\schemas\flashcards.py`

```python
from pydantic import BaseModel
from typing import List


class Flashcard(BaseModel):
    front: str
    back: str


class FlashcardSetResponse(BaseModel):
    set_id: int
    subject: str
    chapter: str
    cards: List[Flashcard]

```

---

### `backend\app\models\notes.py`

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.sql import func
from app.db.session import Base


class GeneratedNote(Base):
    __tablename__ = "generated_notes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    subject = Column(String(255), nullable=False)
    chapter = Column(String(255), nullable=False)
    difficulty = Column(String(50), nullable=False)

    content = Column(String, nullable=False)  # KaTeX-safe raw markdown

    is_saved = Column(Boolean, default=False)
    is_synced = Column(Boolean, default=False)

    is_student_generated = Column(Boolean, default=True)
    is_teacher_provided = Column(Boolean, default=False)

    extra_data = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

```

---

### `backend\app\routers\student\notes.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.schemas.notes import NotesGenerateRequest, NotesResponse
from app.services.notes_service import generate_student_notes
from app.services.xp_service import apply_xp_event
from app.routers.student._guards import student_guard
from app.security import get_current_user
from app.models.user import User
from app.models.notes import GeneratedNote

router = APIRouter(prefix="/api/student/notes", tags=["Student Notes"], dependencies=[student_guard])


@router.post("/generate")
async def generate_notes_endpoint(
    payload: NotesGenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    response = await generate_student_notes(payload, db, current_user)
    await apply_xp_event(db, user_id=1, event="NOTES_GENERATED")
    return response

@router.get("/")
async def list_student_notes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(GeneratedNote).where(
            GeneratedNote.user_id == current_user.id,
            GeneratedNote.is_student_generated == True,
        )
    )

    notes = result.scalars().all()

    return [
        {
            "id": n.id,
            "subject": n.subject,
            "chapter": n.chapter,
            "difficulty": n.difficulty,
            "created_at": n.created_at,
        }
        for n in notes
    ]

```

---

### `backend\app\routers\teacher\notes.py`

```python
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal

from app.db.session import get_db
from app.routers.teacher._guards import teacher_guard
from app.schemas.notes import NotesGenerateRequest, NotesResponse
from app.services.teacher_notes_service import (
    create_manual_notes,
    generate_teacher_notes,
    upload_notes_file,
)

router = APIRouter(
    prefix="/api/teacher/notes",
    tags=["Teacher Notes"],
    dependencies=[teacher_guard],
)


@router.post("/create")
async def create_notes(
    payload: NotesGenerateRequest,
    creation_mode: Literal["MANUAL", "AI_ASSISTED"],
    db: AsyncSession = Depends(get_db),
):
    """
    MANUAL → teacher writes content fully
    AI_ASSISTED → teacher provides outline, AI expands
    """
    if creation_mode == "AI_ASSISTED":
        return await generate_teacher_notes(payload, db)

    return await create_manual_notes(payload, db)


@router.post("/upload")
async def upload_notes(
    subject: str,
    chapter: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload teacher-created notes (PDF).
    """
    return await upload_notes_file(subject, chapter, file, db)

```

---

### `backend\app\schemas\notes.py`

```python
from pydantic import BaseModel
from typing import Optional
from app.schemas.common import ClientContext


class NotesGenerateRequest(BaseModel):
    subject: str
    chapter: str
    difficulty: str
    raw_ai_output: str
    context: ClientContext


class NotesResponse(BaseModel):
    content_id: str
    summary: str
    pdf_url: Optional[str] = None
    offline_ready: bool
    expires_at: Optional[str] = None
```

---

### `backend\app\models\progress.py`

```python
from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    stats = Column(JSON, default=dict)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="progress")

```

---

### `backend\app\routers\parent\progress.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.parent_overview_service import get_detailed_progress

router = APIRouter(prefix="/api/parent/progress", tags=["Parent Progress"])


@router.get("/child/{student_id}")
async def parent_child_progress(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Detailed progress breakdown for a parent.
    """
    return await get_detailed_progress(student_id, db)

```

---

### `backend\app\routers\student\progress.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.progress import Progress
from app.routers.student._guards import student_guard

router = APIRouter(prefix="/api/student/progress", tags=["Student Progress"], dependencies=[student_guard])


@router.get("/")
async def get_progress(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Progress).where(Progress.user_id == 1))
    progress = result.scalar_one_or_none()

    return progress or {"xp": 0, "level": 1, "stats": {}}

```

---

### `backend\app\schemas\progress.py`

```python
from pydantic import BaseModel


class ProgressResponse(BaseModel):
    xp: int
    level: int
    stats: dict | None = None

```

---

### `backend\app\models\subject.py`

```python
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from app.db.session import Base


class SubjectType(str, enum.Enum):
    core = "core"
    elective = "elective"
    extracurricular = "extracurricular"


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    type = Column(Enum(SubjectType), nullable=False)

    # Core subjects only
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=True)

    # Exactly one teacher
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # 🔽 Phase 2.4 additions (nullable by design)
    max_students = Column(Integer, nullable=True)
    enrollment_open_at = Column(DateTime, nullable=True)
    enrollment_close_at = Column(DateTime, nullable=True)

    teacher = relationship("User", foreign_keys=[teacher_id])

```

---

### `backend\app\schemas\subject.py`

```python
from pydantic import BaseModel
from typing import Optional
from enum import Enum


class SubjectType(str, Enum):
    core = "core"
    elective = "elective"


class SubjectCreateRequest(BaseModel):
    name: str
    type: SubjectType
    class_id: Optional[int] = None
    teacher_id: int


class SubjectResponse(BaseModel):
    id: int
    name: str
    type: SubjectType
    class_id: Optional[int]
    teacher_id: int

```

---

### `backend\app\models\subject_student.py`

```python
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.db.session import Base


class SubjectStudent(Base):
    __tablename__ = "subject_students"

    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("subject_id", "student_id", name="uq_subject_student"),
    )

```

---

### `backend\app\models\test.py`

```python
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)

    subject_id = Column(
        Integer,
        ForeignKey("subjects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    questions = relationship("TestQuestion", back_populates="test", cascade="all, delete")
    created_by_student_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    difficulty = Column(String(length=20), nullable=False)

    total_questions = Column(Integer, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


```

---

### `backend\app\models\test_answer.py`

```python
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from app.db.session import Base


class TestAnswer(Base):
    __tablename__ = "test_answers"

    id = Column(Integer, primary_key=True, index=True)

    test_attempt_id = Column(
        Integer,
        ForeignKey("test_attempts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    question_id = Column(Integer, nullable=False)
    
    selected_answer = Column(String(length=255), nullable=False)

    is_correct = Column(Boolean, nullable=False)

```

---

### `backend\app\models\test_attempt.py`

```python
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class TestAttempt(Base):
    __tablename__ = "test_attempts"

    id = Column(Integer, primary_key=True, index=True)

    test_id = Column(
        Integer,
        ForeignKey("tests.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    student_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    score = Column(Integer, nullable=False)
    percentage = Column(Integer, nullable=False)

    submitted_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

```

---

### `backend\app\models\test_question.py`

```python
from sqlalchemy import Column, Integer, ForeignKey, Text, JSON, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class TestQuestion(Base):
    __tablename__ = "test_questions"

    id = Column(Integer, primary_key=True, index=True)

    test_id = Column(
        Integer,
        ForeignKey("tests.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    test = relationship("Test", back_populates="questions")

    question_text = Column(Text, nullable=False)

    options = Column(JSON, nullable=False)

    correct_answer = Column(String(length=255), nullable=False)

    question_order = Column(Integer, nullable=False)
    
```

---

### `backend\app\models\user.py`

```python
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum


class UserRole(str, enum.Enum):
    student = "student"
    teacher = "teacher"
    parent = "parent"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    class_id = Column(Integer, ForeignKey("classes.id"), nullable=True)

    progress = relationship("Progress", back_populates="user", uselist=False)
    total_xp = Column(Integer, nullable=False, server_default="0")
    level = Column(Integer, nullable=False, server_default="1")


```

---

### `backend\app\schemas\user.py`

```python
from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    role: str
    full_name: str
    email: str
    grade: str | None = None
    board: str | None = None


class UserResponse(UserBase):
    pass

```

---

### `backend\app\rag\context_builder.py`

```python
from typing import List


def build_context(chunks: List[str], max_tokens: int = 1500) -> str:
    """
    Builds a bounded context string from retrieved chunks.
    Hard token budgeting to prevent prompt overflow.
    """

    context = []
    token_estimate = 0

    for chunk in chunks:
        chunk_tokens = len(chunk.split())
        if token_estimate + chunk_tokens > max_tokens:
            break
        context.append(chunk)
        token_estimate += chunk_tokens

    return "\n\n".join(context)

```

---

### `backend\app\rag\guardrails.py`

```python
def validate_context(context: str) -> str:
    """
    Basic safety guardrails for injected context.
    Prevents empty or malformed prompts.
    """

    if not context.strip():
        raise ValueError("Empty retrieval context")

    return context

```

---

### `backend\app\rag\retriever.py`

```python
from typing import List


class VectorRetriever:
    """
    Abstract retriever interface.
    Concrete implementations can use FAISS, pgvector, etc.
    """

    async def retrieve(self, query: str, limit: int = 5) -> List[str]:
        raise NotImplementedError("Vector retrieval not implemented")

```

---

### `backend\app\repositories\assignment_repo.py`

```python
from ..models.assignments import Assignment
from .base_repo import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession


class AssignmentRepo(BaseRepo[Assignment]):
    def __init__(self):
        super().__init__(Assignment)

```

---

### `backend\app\repositories\base_repo.py`

```python
from typing import Generic, TypeVar, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import as_declarative

T = TypeVar("T")


class BaseRepo(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    async def get(self, db: AsyncSession, id: int):
        stmt = select(self.model).where(self.model.id == id)
        result = await db.execute(stmt)
        return result.scalars().first()

    async def list(self, db: AsyncSession, limit: int = 100):
        stmt = select(self.model).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj):
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj
```

---

### `backend\app\repositories\flashcard_repo.py`

```python
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

```

---

### `backend\app\repositories\note_repo.py`

```python
from ..models.notes import GeneratedNote
from .base_repo import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession


class NoteRepo(BaseRepo[GeneratedNote]):
    def __init__(self):
        super().__init__(GeneratedNote)

    async def create_note(self, db: AsyncSession, **kwargs):
        n = GeneratedNote(**kwargs)
        return await self.create(db, n)

```

---

### `backend\app\routers\analytics.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.security import get_current_user
from app.models.user import User, UserRole
from app.services.analytics_service import AnalyticsService
from app.services.analytics_student_service import StudentAnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview")
async def analytics_overview(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == UserRole.teacher:
        return {
            "scope": "teacher",
            "class": await AnalyticsService.class_overview(
                db=db, class_id=current_user.class_id
            ),
            "subjects": await AnalyticsService.subject_overview(db=db),
        }

    if current_user.role == UserRole.student:
        return {
            "scope": "student",
            "data": await AnalyticsService.student_overview(
                db=db, student_id=current_user.id
            ),
        }

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Analytics not available for this role",
    )
@router.get("/students")
async def analytics_students(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.teacher:
        raise HTTPException(status_code=403)

    return await StudentAnalyticsService.class_students_overview(
        db=db,
        class_id=current_user.class_id,
    )
```

---

### `backend\app\routers\analytics_export.py`

```python
import csv
from io import StringIO
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.security import get_current_user
from app.models.user import User, UserRole
from app.services.analytics_student_service import StudentAnalyticsService

router = APIRouter(prefix="/analytics/export", tags=["Analytics Export"])


@router.get("/students.csv")
async def export_students_csv(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.teacher:
        raise HTTPException(status_code=403)

    students = await StudentAnalyticsService.class_students_overview(
        db=db,
        class_id=current_user.class_id,
    )

    buffer = StringIO()
    writer = csv.DictWriter(
        buffer,
        fieldnames=students[0].keys() if students else []
    )
    writer.writeheader()
    writer.writerows(students)

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=class_analytics.csv"},
    )

```

---

### `backend\app\routers\auth.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.auth import SignupRequest, LoginRequest, AuthResponse
from app.services.auth_service import signup_user, login_user
from sqlalchemy import select
from app.models.user import User
from app.security.jwt import create_access_token, create_refresh_token
from jose import JWTError
from app.security.passwords import verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
async def signup(
    data: SignupRequest,
    db: AsyncSession = Depends(get_db),
):
    user = await signup_user(data, db)
    return {"id": user.id, "role": user.role}


@router.post("/login")
async def login(payload: dict, db: AsyncSession = Depends(get_db)):
    email = payload.get("email")
    password = payload.get("password")

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        {"sub": str(user.id), "role": user.role}
    )
    refresh_token = create_refresh_token(
        {"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "role": user.role,
            "class_id": user.class_id,
        },
    }


@router.post("/refresh")
async def refresh(payload: dict):
    from app.security.jwt import decode_token

    token = payload.get("refresh_token")

    try:
        data = decode_token(token)
        if data.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user_id = data.get("sub")
        access_token = create_access_token({"sub": user_id})

        return {"access_token": access_token}
    except JWTError:
        raise HTTPException(status_code=401, detail="Expired refresh token")
```

---

### `backend\app\schemas\auth.py`

```python
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.security.roles import Role


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    role: str  # student | teacher
    registration_code: Optional[str] = None  # student only


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    role: Role
    class_id: Optional[int]

```

---

### `backend\app\routers\subjects.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.subject import SubjectCreateRequest, SubjectResponse
from app.services.subject_service import create_subject
from app.security.dependencies import require_role
from app.models.user import UserRole

router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"],
)


@router.post(
    "",
    response_model=SubjectResponse,
    dependencies=[Depends(require_role(UserRole.admin))]
)
async def create_subject_endpoint(
    payload: SubjectCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    return await create_subject(payload, db)

```

---

### `backend\app\routers\student\subjects.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.security import get_current_user
from app.models.user import User, UserRole
from app.models.subject import Subject


router = APIRouter(prefix="/student/subjects", tags=["Student Subjects"])


@router.get("")
async def list_subjects_for_student(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can view subjects",
        )

    result = await db.execute(select(Subject))
    subjects = result.scalars().all()

    return [{"id": s.id, "name": s.name} for s in subjects]

```

---

### `backend\app\routers\teacher_tests.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.security import get_current_user
from app.models.user import User, UserRole
from app.models.subject import Subject
from app.models.test import Test
from app.models.test_attempt import TestAttempt
from app.schemas.teacher_results import StudentTestResult


router = APIRouter(prefix="/teacher/tests", tags=["Teacher Tests"])


@router.get(
    "/subject/{subject_id}/results",
    response_model=list[StudentTestResult],
)
async def get_subject_results(
    subject_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # -------------------------------------------------
    # Role check
    # -------------------------------------------------
    if current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can view test results",
        )

    # -------------------------------------------------
    # Validate subject ownership
    # -------------------------------------------------
    subject_result = await db.execute(
        select(Subject).where(
            Subject.id == subject_id,
            Subject.teacher_id == current_user.id,
        )
    )
    subject = subject_result.scalar_one_or_none()

    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found or not assigned to teacher",
        )

    # -------------------------------------------------
    # Fetch tests for subject
    # -------------------------------------------------
    tests_result = await db.execute(
        select(Test).where(Test.subject == subject.name)
    )
    tests = tests_result.scalars().all()

    if not tests:
        return []

    test_ids = [t.id for t in tests]

    # -------------------------------------------------
    # Fetch attempts + student info
    # -------------------------------------------------
    attempts_result = await db.execute(
        select(
            TestAttempt,
            User.id,
            User.name,
            Test.title,
        )
        .join(User, User.id == TestAttempt.student_id)
        .join(Test, Test.id == TestAttempt.test_id)
        .where(TestAttempt.test_id.in_(test_ids))
    )

    results: list[StudentTestResult] = []

    for attempt, student_id, student_name, test_title in attempts_result.all():
        results.append(
            StudentTestResult(
                student_id=student_id,
                student_name=student_name,
                test_id=attempt.test_id,
                test_title=test_title,
                score=attempt.score,
                submitted_at=attempt.submitted_at,
            )
        )

    return results

```

---

### `backend\app\routers\admin\content.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.assignments import Assignment
from app.models.test import Test

router = APIRouter(prefix="/api/admin/content", tags=["Admin Content"])


@router.get("/assignments")
async def admin_list_assignments(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Assignment))
    return result.scalars().all()


@router.get("/tests")
async def admin_list_tests(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Test))
    return result.scalars().all()

```

---

### `backend\app\routers\admin\system.py`

```python
from fastapi import APIRouter
from app.config import get_settings

router = APIRouter(prefix="/api/admin/system", tags=["Admin System"])


@router.get("/config")
async def admin_system_config():
    """
    Returns non-sensitive runtime configuration.
    """
    settings = get_settings()
    return {
        "app_name": settings.APP_NAME,
        "env": settings.APP_ENV,
        "debug": settings.DEBUG,
        "log_level": settings.LOG_LEVEL,
    }

```

---

### `backend\app\routers\admin\users.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.admin_user_service import (
    list_users,
    get_user,
    update_user_role,
    disable_user,
)

router = APIRouter(prefix="/api/admin/users", tags=["Admin Users"])


@router.get("/")
async def admin_list_users(
    db: AsyncSession = Depends(get_db),
):
    return await list_users(db)


@router.get("/{user_id}")
async def admin_get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await get_user(user_id, db)


@router.post("/{user_id}/role")
async def admin_update_user_role(
    user_id: int,
    role: str,
    db: AsyncSession = Depends(get_db),
):
    return await update_user_role(user_id, role, db)


@router.post("/{user_id}/disable")
async def admin_disable_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await disable_user(user_id, db)

```

---

### `backend\app\routers\admin\_guards.py`

```python
from fastapi import Depends
from app.security import require_role
from app.security.roles import Role

admin_guard = Depends(require_role(Role.admin))

```

---

### `backend\app\routers\parent\_guards.py`

```python
from fastapi import Depends
from app.security import require_role
from app.security.roles import Role

parent_guard = Depends(require_role(Role.parent))

```

---

### `backend\app\routers\student\_guards.py`

```python
from fastapi import Depends
from app.security import require_role
from app.security.roles import Role

student_guard = Depends(require_role(Role.student))

```

---

### `backend\app\routers\teacher\_guards.py`

```python
from fastapi import Depends
from app.security import require_role
from app.security.roles import Role

teacher_guard = Depends(require_role(Role.teacher))

```

---

### `backend\app\routers\parent\insights.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.parent_insights_service import get_parent_insights

router = APIRouter(prefix="/api/parent/insights", tags=["Parent Insights"])


@router.get("/child/{student_id}")
async def parent_ai_insights(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    AI-generated academic insights for parents.
    """
    return await get_parent_insights(student_id, db)

```

---

### `backend\app\routers\parent\overview.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.parent_overview_service import get_parent_overview

router = APIRouter(prefix="/api/parent/overview", tags=["Parent Overview"])


@router.get("/child/{student_id}")
async def parent_child_overview(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    High-level academic overview for a parent.
    """
    return await get_parent_overview(student_id, db)

```

---

### `backend\app\routers\student\ai_chat.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers.student._guards import student_guard

from app.db.session import get_db
from app.schemas.common import ClientContext
from app.services.ai_service import chat_with_ai
from app.services.xp_service import apply_xp_event

router = APIRouter(prefix="/api/student/ai", tags=["Student AI Chat"], dependencies=[student_guard])


@router.post("/chat")
async def ai_chat_endpoint(
    messages: list[dict],
    context: ClientContext,
    db: AsyncSession = Depends(get_db),
):
    response = await chat_with_ai(messages, context)
    await apply_xp_event(db, user_id=1, event="AI_CHAT_INTERACTION")
    return {"response": response}

```

---

### `backend\app\routers\student\notes_storage.py`

```python
from fastapi import APIRouter, Depends, HTTPException
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



@router.get("/{note_id}/download")
async def download_note(note_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(GeneratedNote).where(GeneratedNote.id == note_id)
    )
    note = result.scalar_one_or_none()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return PlainTextResponse(
        note.extra_data["content"],
        media_type="text/markdown",
        headers={
            "Content-Disposition": f'attachment; filename="notes_{note_id}.md"'
        },
    )

```

---

### `backend\app\routers\student\sync.py`

```python
from fastapi import APIRouter
from app.schemas.sync import SyncRequest, SyncResponse
from app.services.sync_service import get_available_sync_items
from app.routers.student._guards import student_guard

router = APIRouter(prefix="/api/student/sync", tags=["Student Sync"], dependencies=[student_guard])


@router.post("/available", response_model=SyncResponse)
async def available_sync_items(payload: SyncRequest):
    return await get_available_sync_items(
        last_sync_at=payload.last_sync_at,
        client_known_ids=payload.client_known_ids,
    )

```

---

### `backend\app\schemas\sync.py`

```python
from pydantic import BaseModel
from typing import List, Optional


class SyncItem(BaseModel):
    content_id: str
    content_type: str  # notes | flashcards | tests
    version: str
    updated_at: str


class SyncRequest(BaseModel):
    last_sync_at: Optional[str] = None
    client_known_ids: List[str] = []


class SyncResponse(BaseModel):
    available: List[SyncItem]

```

---

### `backend\app\routers\student\teacher_notes.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.notes import GeneratedNote
from app.routers.student._guards import student_guard
from fastapi.responses import FileResponse
from app.security import get_current_user
from app.models.user import User
from app.models.notes import GeneratedNote

router = APIRouter(
    prefix="/api/student/notes",
    tags=["Student Teacher Notes"],
    dependencies=[student_guard],
    redirect_slashes=False,
)


@router.get("/teacher")
async def list_teacher_notes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(GeneratedNote).where(
            GeneratedNote.is_teacher_provided == True
        )
    )

    notes = result.scalars().all()

    return [
        {
            "id": n.id,
            "subject": n.subject,
            "chapter": n.chapter,
        }
        for n in notes
    ]



@router.get("/{note_id}")
async def get_teacher_note(note_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(GeneratedNote).where(
            GeneratedNote.id == note_id,
            GeneratedNote.is_teacher_provided == True,
        )
    )

    note = result.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    # PDF-based note
    if note.pdf_url:
        return {
            "type": "pdf",
            "url": note.pdf_url,
        }

    # AI / manual content
    return {
        "type": "markdown",
        "content": note.extra_data.get("content"),
    }


@router.get("/{note_id}/download")
async def download_teacher_note(note_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(GeneratedNote).where(
            GeneratedNote.id == note_id,
            GeneratedNote.is_teacher_provided == True,
        )
    )

    note = result.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.pdf_url:
        return FileResponse(note.pdf_url)

    return {
        "content": note.extra_data.get("content"),
    }

```

---

### `backend\app\routers\student\tests.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.test_attempt import TestAttempt
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.services.teacher_test_service import create_test_ai_assisted
from app.schemas.tests import TestCreateRequest
from app.security import get_current_user
from app.models.user import User, UserRole
from app.models.test import Test
from app.schemas.test_submission import (
    TestSubmissionRequest,
    TestSubmissionResponse,
)
from app.services.test_evaluation_service import evaluate_test_submission


router = APIRouter(prefix="/student/tests", tags=["Student Tests"])


@router.get("/{test_id}")
async def get_test_for_student(
    test_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Test)
        .options(selectinload(Test.questions))
        .where(Test.id == test_id)
    )

    test = result.scalar_one_or_none()

    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    questions = [
        {
            "id": q.id,
            "question": q.question_text,
            "options": q.options,
        }
        for q in sorted(test.questions, key=lambda x: x.question_order)
    ]

    return {
        "id": test.id,
        "subject_id": test.subject_id,
        "difficulty": test.difficulty,
        "total_questions": test.total_questions,
        "questions": questions,
    }



@router.post(
    "/{test_id}/submit",
    response_model=TestSubmissionResponse,
)
async def submit_test(
    test_id: int,
    payload: TestSubmissionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can submit tests",
        )

    result = await evaluate_test_submission(
        test_id=test_id,
        submitted_answers=payload.answers,
        db=db,
        current_user=current_user,
    )

    return result


@router.get("")
async def list_tests_for_student(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can view tests",
        )

    result = await db.execute(
        select(Test)
        .options(selectinload(Test.questions))
    )

    tests = result.scalars().all()

    response = []

    for t in tests:
        # Fetch attempts for this student & test
        attempts_result = await db.execute(
            select(
                func.max(TestAttempt.score),
                func.count(TestAttempt.id),
            ).where(
                TestAttempt.test_id == t.id,
                TestAttempt.student_id == current_user.id,
            )
        )
        best_score, attempt_count = attempts_result.one()

        questions = [
            {
                "id": q.id,
                "question": q.question_text,
                "options": q.options,
            }
            for q in t.questions
        ]


        response.append(
            {
                "id": t.id,
                "title": t.title,
                "subject_id": t.subject_id,
                "difficulty": t.difficulty,
                "total_questions": len(questions),

                # --------- Aggregated fields ---------
                "duration": len(questions),
                "xp_reward": 0,                 # XP shell untouched
                "is_completed": attempt_count > 0,
                "best_score": best_score,
            }
        )

    return response

@router.post("/generate")
async def generate_test_for_student(
    payload: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can generate tests",
        )

    subject_id = payload.get("subject_id")
    chapter = payload.get("chapter")
    subject = payload.get("subject")

    if not subject_id or not chapter:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="subject_id and chapter are required",
        )

    # Reuse existing AI-assisted test creation
    test_request = TestCreateRequest(
        title=f"Practice Test - {chapter}",
        subject_id=subject_id,
        subject = subject,
        difficulty="medium",
        chapter=chapter,
        ai_assisted=True,
    )

    test = await create_test_ai_assisted(test_request, db, current_user)
    return {"id": test.id, "title": test.title}



```

---

### `backend\app\routers\teacher\tests.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal

from app.db.session import get_db
from app.schemas.tests import TestCreateRequest, TestResponse
from app.services.teacher_test_service import (
    create_test_manual,
    create_test_ai_assisted,
)
from app.routers.teacher._guards import teacher_guard
from app.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/teacher/tests", tags=["Teacher Tests"])


@router.post("/create", response_model=TestResponse)
async def create_test_endpoint(
    payload: TestCreateRequest,
    creation_mode: Literal["MANUAL", "AI_ASSISTED"],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    creation_mode:
    - MANUAL → teacher provides all questions
    - AI_ASSISTED → AI suggests questions & answers
    """
    if creation_mode == "AI_ASSISTED":
        return await create_test_ai_assisted(payload, db, current_user)

    return await create_test_manual(payload, db)

```

---

### `backend\app\schemas\tests.py`

```python
from pydantic import BaseModel
from typing import List


class TestQuestion(BaseModel):
    question: str
    options: List[str]
    correct_option: int


class TestCreateRequest(BaseModel):
    title: str
    subject_id: int
    subject: str
    chapter: str
    difficulty: str
    ai_assisted: bool


class TestResponse(BaseModel):
    test_id: int
    title: str
    total_marks: int

```

---

### `backend\app\routers\teacher\ai_tools.py`

```python
from fastapi import APIRouter
from app.schemas.common import ClientContext
from app.services.teacher_ai_service import (
    suggest_test_questions,
    suggest_assignment_outline,
)
from app.routers.teacher._guards import teacher_guard

router = APIRouter(prefix="/api/teacher/ai", tags=["Teacher AI Tools"])


@router.post("/suggest/test")
async def ai_suggest_test_questions(
    subject: str,
    difficulty: str,
    context: ClientContext,
):
    return await suggest_test_questions(subject, difficulty, context)


@router.post("/suggest/assignment")
async def ai_suggest_assignment(
    subject: str,
    topic: str,
    context: ClientContext,
):
    return await suggest_assignment_outline(subject, topic, context)

```

---

### `backend\app\routers\teacher\reports.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.teacher_report_service import get_student_report
from app.routers.teacher._guards import teacher_guard

router = APIRouter(prefix="/api/teacher/reports", tags=["Teacher Reports"])


@router.get("/student/{student_id}")
async def get_detailed_student_report(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Returns a detailed academic + behavioral report for a student.
    """
    return await get_student_report(student_id, db)

```

---

### `backend\app\routers\teacher\students.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.security.dependencies import require_role, get_current_user
from app.models.user import UserRole
from app.services.teacher_context import get_teacher_subject
from app.services.teacher_student_service import get_students_for_subject

router = APIRouter(
    prefix="/teacher/students",
    tags=["Teacher"],
    dependencies=[Depends(require_role(UserRole.teacher))],
)


@router.get("")
async def list_students_for_teacher(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    subject = await get_teacher_subject(current_user.id, db)
    students = await get_students_for_subject(subject, db)

    return [
        {
            "id": student.id,
            "email": student.email,
            "class_id": student.class_id,
        }
        for student in students
    ]

```

---

### `backend\app\schemas\common.py`

```python
from pydantic import BaseModel
from typing import Literal, Optional


class ClientContext(BaseModel):
    client_type: Literal["mobile", "desktop"]
    connectivity: Literal["online", "offline"]
    model_capability: Literal["light", "heavy"]
    cache_allowed: bool = True
    max_payload_kb: Optional[int] = None

```

---

### `backend\app\schemas\teacher_results.py`

```python
from pydantic import BaseModel
from datetime import datetime


class StudentTestResult(BaseModel):
    student_id: int
    student_name: str
    test_id: int
    test_title: str
    score: int
    submitted_at: datetime

```

---

### `backend\app\schemas\test_submission.py`

```python
from pydantic import BaseModel
from typing import List


class QuestionResult(BaseModel):
    question_index: int
    is_correct: bool


class AnswerSubmission(BaseModel):
    question_id: int
    selected_answer: str


class TestSubmissionRequest(BaseModel):
    answers: list[AnswerSubmission]


class TestSubmissionResponse(BaseModel):
    score: int
    total_questions: int
    percentage: int
    results: List[QuestionResult]

```

---

### `backend\app\security\admin_guard.py`

```python
from fastapi import HTTPException, status


def require_admin(role: str):
    """
    Enforces admin-only access.
    Replace role source with auth context later.
    """
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )

```

---

### `backend\app\security\dependencies.py`

```python
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError
from app.security.oauth2 import bearer_scheme
from fastapi.security import OAuth2PasswordBearer

from app.db.session import get_db
from app.models.user import User
from app.security.roles import Role
from app.security.jwt import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    try:
        payload = decode_token(token)

        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired or invalid",
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user


def require_role(*roles: Role):
    async def role_guard(user=Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return user

    return role_guard

```

---

### `backend\app\security\guards.py`

```python
from fastapi import HTTPException
from app.schemas.common import ClientContext


def enforce_client_capabilities(context: ClientContext) -> None:
    """
    Prevents misuse of heavy models or server-only features.
    """

    if context.connectivity == "offline" and context.model_capability == "heavy":
        raise HTTPException(
            status_code=400,
            detail="Heavy model access not allowed in offline mode",
        )

```

---

### `backend\app\security\jwt.py`

```python
from dotenv import load_dotenv
load_dotenv()
import os
from datetime import datetime, timedelta
from jose import jwt, JWTError

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY environment variable is not set")

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


# ------------------------------------------------------------------
# Token creators
# ------------------------------------------------------------------

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["type"] = "access"
    to_encode["exp"] = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    to_encode = data.copy()
    to_encode["type"] = "refresh"
    to_encode["exp"] = datetime.utcnow() + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ------------------------------------------------------------------
# Token decoder
# ------------------------------------------------------------------

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
```

---

### `backend\app\security\oauth2.py`

```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_scheme = HTTPBearer(auto_error=True)

```

---

### `backend\app\security\passwords.py`

```python
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """
    Hash password using Argon2.
    - No length limits
    - Secure against GPU attacks
    - Compatible with bcrypt>=4 (Chromadb)
    """
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

```

---

### `backend\app\security\rate_limiter.py`

```python
import time
from fastapi import HTTPException, Request

# Simple in-memory rate limiter (replace with Redis in production)
RATE_LIMIT = 30  # requests
WINDOW_SECONDS = 60

_client_requests: dict[str, list[float]] = {}


def rate_limit(request: Request) -> None:
    client_ip = request.client.host
    now = time.time()

    timestamps = _client_requests.get(client_ip, [])
    timestamps = [t for t in timestamps if now - t < WINDOW_SECONDS]

    if len(timestamps) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later.",
        )

    timestamps.append(now)
    _client_requests[client_ip] = timestamps

```

---

### `backend\app\security\roles.py`

```python
from app.models.user import UserRole as Role
from fastapi import Depends, HTTPException
from app.models.user import User
from app.security.dependencies import get_current_user


def require_role(*roles: str):
    async def role_guard(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return role_guard
```

---

### `backend\app\services\admin_system_service.py`

```python
from app.config import get_settings


async def get_system_status():
    settings = get_settings()

    return {
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "debug": settings.DEBUG,
        "ollama_base": settings.OLLAMA_BASE_URL,
    }

```

---

### `backend\app\services\admin_user_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User


async def list_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()


async def get_user(user_id: int, db: AsyncSession):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        return {"error": "User not found"}
    return user


async def update_user_role(
    user_id: int,
    role: str,
    db: AsyncSession,
):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        return {"error": "User not found"}

    user.role = role
    await db.commit()
    await db.refresh(user)

    return {
        "user_id": user.id,
        "new_role": user.role,
    }


async def disable_user(
    user_id: int,
    db: AsyncSession,
):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        return {"error": "User not found"}

    user.is_active = False
    await db.commit()

    return {
        "user_id": user.id,
        "disabled": True,
    }

```

---

### `backend\app\services\ai_service.py`

```python
from typing import List, Dict
from app.ai import OllamaClient, select_model
from app.schemas.common import ClientContext

ollama = OllamaClient()


def _build_chat_prompt(messages: List[Dict[str, str]]) -> str:
    """
    Converts chat history into a single prompt.
    Expected message format:
    { "role": "user" | "assistant", "content": str }
    """

    prompt_lines = [
        "You are a helpful, accurate AI tutor for school students.",
        "Follow the syllabus strictly.",
        "Do not hallucinate.",
        "Explain concepts clearly and simply.",
        "",
        "Conversation:",
    ]

    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "").strip()
        if not content:
            continue
        prompt_lines.append(f"{role.capitalize()}: {content}")

    prompt_lines.append("Assistant:")

    return "\n".join(prompt_lines)


async def chat_with_ai(
    messages: List[Dict[str, str]],
    context: ClientContext,
) -> str:
    """
    Main AI chat entry point for students.
    """

    model = select_model(context)
    prompt = _build_chat_prompt(messages)

    response = await ollama.generate(
        prompt=prompt,
        model_name=model,
        temperature=0.25,
        max_tokens=900 if context.client_type == "mobile" else 1400,
    )

    return response.strip()

```

---

### `backend\app\services\analytics_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.test_attempt import TestAttempt
from app.models.test import Test
from app.models.user import User
from app.services.analytics_student_service import StudentAnalyticsService

class AnalyticsService:
    """
    Centralized read-only analytics service.
    Uses BOTH score and percentage.
    """

    @staticmethod
    async def student_overview(db: AsyncSession, student_id: int) -> dict:
        result = await db.execute(
            select(
                func.count(TestAttempt.id).label("attempts"),
                func.avg(TestAttempt.score).label("avg_score"),
                func.avg(TestAttempt.percentage).label("avg_percentage"),
            ).where(TestAttempt.student_id == student_id)
        )

        row = result.one()

        return {
            "attempts": row.attempts or 0,
            "average_score": round(row.avg_score or 0, 2),
            "average_percentage": round(row.avg_percentage or 0, 2),
        }

    @staticmethod
    async def class_overview(db: AsyncSession, class_id: int) -> dict:
        result = await db.execute(
            select(
                func.count(func.distinct(TestAttempt.student_id)).label("students"),
                func.avg(TestAttempt.score).label("avg_score"),
                func.avg(TestAttempt.percentage).label("avg_percentage"),
            )
            .join(User, User.id == TestAttempt.student_id)
            .where(User.class_id == class_id)
        )

        row = result.one()

        return {
            "students": row.students or 0,
            "average_score": round(row.avg_score or 0, 2),
            "average_percentage": round(row.avg_percentage or 0, 2),
        }

    @staticmethod
    async def subject_overview(db: AsyncSession) -> list[dict]:
        result = await db.execute(
            select(
                Test.subject,
                func.avg(TestAttempt.score).label("avg_score"),
                func.avg(TestAttempt.percentage).label("avg_percentage"),
                func.count(TestAttempt.id).label("attempts"),
            )
            .join(Test, Test.id == TestAttempt.test_id)
            .group_by(Test.subject)
        )

        return [
            {
                "subject": row.subject,
                "average_score": round(row.avg_score or 0, 2),
                "average_percentage": round(row.avg_percentage or 0, 2),
                "attempts": row.attempts,
            }
            for row in result.all()
        ]
```

---

### `backend\app\services\analytics_student_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.test_attempt import TestAttempt
from app.models.user import User


class StudentAnalyticsService:
    @staticmethod
    async def class_students_overview(
        db: AsyncSession,
        class_id: int,
    ) -> list[dict]:
        result = await db.execute(
            select(
                User.id,
                User.name,
                func.count(TestAttempt.id).label("attempts"),
                func.avg(TestAttempt.score).label("avg_score"),
                func.avg(TestAttempt.percentage).label("avg_percentage"),
            )
            .join(TestAttempt, TestAttempt.student_id == User.id, isouter=True)
            .where(User.class_id == class_id)
            .group_by(User.id)
        )

        return [
            {
                "student_id": r.id,
                "name": r.name,
                "attempts": r.attempts or 0,
                "average_score": round(r.avg_score or 0, 2),
                "average_percentage": round(r.avg_percentage or 0, 2),
            }
            for r in result.all()
        ]

```

---

### `backend\app\services\auth_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.user import User, UserRole
from app.models.classroom import Classroom
from app.models.progress import Progress
from app.schemas.auth import SignupRequest, LoginRequest
from app.security.passwords import hash_password, verify_password
from app.security.jwt import create_access_token

def parse_registration_code(code: str):
    if len(code) != 6 or not code.isdigit():
        raise HTTPException(status_code=400, detail="Invalid registration code")

    grade = int(code[:2])
    section_num = code[2:4]
    roll = int(code[4:])

    section_map = {"01": "A", "02": "B", "03": "C"}
    if section_num not in section_map:
        raise HTTPException(status_code=400, detail="Invalid section code")

    return grade, section_map[section_num], roll


async def signup_user(payload: SignupRequest, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == payload.email))
    if result.scalar():
        raise HTTPException(status_code=400, detail="Email already registered")

    class_id = None

    if payload.role == "student":
        if not payload.registration_code:
            raise HTTPException(status_code=400, detail="Registration code required")

        grade, section, _ = parse_registration_code(payload.registration_code)
        prefix = payload.registration_code[:4]

        result = await db.execute(
            select(Classroom).where(Classroom.code_prefix == prefix)
        )
        classroom = result.scalar()

        if not classroom:
            classroom = Classroom(
                grade=grade,
                section=section,
                code_prefix=prefix,
            )
            db.add(classroom)
            await db.flush()

        class_id = classroom.id

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=UserRole(payload.role),
        class_id=class_id,
    )
    db.add(user)
    await db.flush()

    if payload.role == "student":
        progress = Progress(user_id=user.id)
        db.add(progress)

    await db.commit()

    return {
        "user_id": user.id,
        "role": user.role.value,
        "class_id": user.class_id,
    }


async def login_user(data: LoginRequest, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token({
        "sub": user.id,
        "role": user.role,
        "class_id": user.class_id
    })

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "role": user.role,
        "class_id": user.class_id
    }
```

---

### `backend\app\services\elective_enrollment_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.subject import Subject
from app.models.subject_student import SubjectStudent
from app.services.enrollment_guard import validate_enrollment_allowed


async def enroll_student_in_subject(
    subject_id: int,
    student_id: int,
    db: AsyncSession,
):
    subject = await db.get(Subject, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    await validate_enrollment_allowed(subject, db)

    # Prevent duplicate enrollment
    result = await db.execute(
        select(SubjectStudent).where(
            SubjectStudent.subject_id == subject_id,
            SubjectStudent.student_id == student_id,
        )
    )
    if result.scalar():
        raise HTTPException(
            status_code=400,
            detail="Student already enrolled in subject",
        )

    enrollment = SubjectStudent(
        subject_id=subject_id,
        student_id=student_id,
    )

    db.add(enrollment)
    await db.commit()

```

---

### `backend\app\services\enrollment_guard.py`

```python
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.subject import Subject, SubjectType
from app.models.subject_student import SubjectStudent


async def validate_enrollment_allowed(
    subject: Subject,
    db: AsyncSession,
):
    """
    Validates whether enrollment is allowed for a subject.
    Does NOT perform enrollment.
    """

    # Core subjects cannot be manually enrolled
    if subject.type == SubjectType.core:
        raise HTTPException(
            status_code=400,
            detail="Enrollment not allowed for core subjects",
        )

    now = datetime.utcnow()

    # Enrollment window validation
    if subject.enrollment_open_at and now < subject.enrollment_open_at:
        raise HTTPException(
            status_code=403,
            detail="Enrollment window has not opened yet",
        )

    if subject.enrollment_close_at and now > subject.enrollment_close_at:
        raise HTTPException(
            status_code=403,
            detail="Enrollment window has closed",
        )

    # Capacity validation
    if subject.max_students is not None:
        result = await db.execute(
            select(func.count())
            .select_from(SubjectStudent)
            .where(SubjectStudent.subject_id == subject.id)
        )
        enrolled_count = result.scalar()

        if enrolled_count >= subject.max_students:
            raise HTTPException(
                status_code=409,
                detail="Subject enrollment is full",
            )

```

---

### `backend\app\services\file_validation.py`

```python
from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = {".pdf"}
MAX_FILE_SIZE_MB = 10


async def validate_upload(file: UploadFile):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    ext = "." + file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed",
        )

    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)

    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail="File exceeds 10MB limit",
        )

    file.file.seek(0)

```

---

### `backend\app\services\flashcards_service.py`

```python
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
"""

    response = await ollama.generate(
        prompt=prompt,
        model_name=model,
        temperature=0.3,
        max_tokens=800,
    )

    cards = [
        {"front": line.split(" - ")[0], "back": line.split(" - ")[1]}
        for line in response.split("\n")
        if " - " in line
    ]

    return FlashcardSetResponse(
        set_id=1,
        subject=subject,
        chapter=chapter,
        cards=cards,
    )

```

---

### `backend\app\services\notes_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai import OllamaClient, select_model
from app.schemas.notes import NotesGenerateRequest, NotesResponse

from fastapi import HTTPException
from app.models.notes import GeneratedNote
from app.models.user import User

ollama = OllamaClient()

LATEX_SAFE_NOTES_PROMPT = """
You are an expert textbook author writing high-quality academic notes.

TASK:
Generate clear, structured, textbook-quality study notes for students.

SUBJECT: {subject}
CHAPTER: {chapter}
DIFFICULTY: {difficulty}

MANDATORY FORMATTING RULES (STRICT):
1. ALL mathematical expressions MUST be written in valid LaTeX.
2. Inline math MUST use: \\( ... \\)
3. Display math MUST use:
   \\[
   ...
   \\]
4. DO NOT use $ or $$.
5. Ensure KaTeX compatibility.

CONTENT STRUCTURE:
- Headings
- Bullet points
- Worked examples
- Exam-focused clarity
"""

async def generate_student_notes(
    payload,
    db: AsyncSession,
    current_user: User,
):
    raw_content = payload.raw_ai_output  # your AI result

    if not raw_content or not raw_content.strip():
        raise HTTPException(status_code=400, detail="AI returned empty content")

    note = GeneratedNote(
        user_id=current_user.id,
        subject=payload.subject,
        chapter=payload.chapter,
        difficulty=payload.difficulty,
        content=raw_content,  # Preserve KaTeX
        is_student_generated=True,
        is_teacher_provided=False,
    )

    db.add(note)
    await db.commit()
    await db.refresh(note)

    return {
        "id": note.id,
        "subject": note.subject,
        "chapter": note.chapter,
        "content": note.content,
        "offline_ready": True,
    }
```

---

### `backend\app\services\parent_insights_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.progress import Progress
from app.ai import OllamaClient

ollama = OllamaClient()


async def get_parent_insights(
    student_id: int,
    db: AsyncSession,
) -> dict:
    """
    Generates read-only academic insights for parents.
    """

    result = await db.execute(
        select(Progress).where(Progress.user_id == student_id)
    )
    progress = result.scalar_one_or_none()

    if not progress:
        return {"insights": "No data available yet."}

    prompt = f"""
You are an educational analyst.

Analyze this student's academic progress and provide insights
for parents in simple, reassuring language.

XP: {progress.xp}
Level: {progress.level}
Stats: {progress.stats}

Rules:
- No recommendations to change syllabus
- No grading judgments
- Supportive tone
"""

    response = await ollama.generate(
        prompt=prompt,
        model_name="mistral:7b-instruct",
        temperature=0.2,
        max_tokens=600,
    )

    return {"insights": response}

```

---

### `backend\app\services\parent_overview_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.progress import Progress
from app.models.assignments import Assignment
from app.models.test import Test


async def get_parent_overview(
    student_id: int,
    db: AsyncSession,
) -> dict:
    """
    High-level snapshot for parents.
    """

    progress_result = await db.execute(
        select(Progress).where(Progress.user_id == student_id)
    )
    progress = progress_result.scalar_one_or_none()

    assignments_result = await db.execute(
        select(Assignment).where(Assignment.created_by == student_id)
    )
    assignments = assignments_result.scalars().all()

    tests_result = await db.execute(
        select(Test).where(Test.created_by == student_id)
    )
    tests = tests_result.scalars().all()

    return {
        "student_id": student_id,
        "xp": progress.xp if progress else 0,
        "level": progress.level if progress else 1,
        "assignments_assigned": len(assignments),
        "tests_attempted": len(tests),
    }


async def get_detailed_progress(
    student_id: int,
    db: AsyncSession,
) -> dict:
    """
    Detailed academic breakdown.
    """

    progress_result = await db.execute(
        select(Progress).where(Progress.user_id == student_id)
    )
    progress = progress_result.scalar_one_or_none()

    return {
        "student_id": student_id,
        "xp": progress.xp if progress else 0,
        "level": progress.level if progress else 1,
        "stats": progress.stats if progress else {},
    }

```

---

### `backend\app\services\pdf_generator.py`

```python
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT


def generate_notes_pdf(
    title: str,
    subject: str,
    chapter: str,
    content: str,
) -> BytesIO:
    """
    Generates a PDF for AI-generated notes and returns an in-memory buffer.
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1 * inch,
        leftMargin=1 * inch,
        topMargin=1 * inch,
        bottomMargin=1 * inch,
    )

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="TitleStyle",
            fontSize=18,
            spaceAfter=16,
            alignment=TA_LEFT,
        )
    )

    styles.add(
        ParagraphStyle(
            name="BodyStyle",
            fontSize=11,
            leading=15,
            spaceAfter=10,
        )
    )

    story = []

    story.append(Paragraph(title, styles["TitleStyle"]))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph(f"<b>Subject:</b> {subject}", styles["BodyStyle"]))
    story.append(Paragraph(f"<b>Chapter:</b> {chapter}", styles["BodyStyle"]))
    story.append(Spacer(1, 0.3 * inch))

    for line in content.split("\n"):
        if line.strip():
            story.append(Paragraph(line, styles["BodyStyle"]))
            story.append(Spacer(1, 0.1 * inch))

    doc.build(story)
    buffer.seek(0)

    return buffer

```

---

### `backend\app\services\subject_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.subject import Subject, SubjectType
from app.models.subject_student import SubjectStudent
from app.models.user import User, UserRole
from app.schemas.subject import SubjectCreateRequest


async def create_subject(payload: SubjectCreateRequest, db: AsyncSession):
    # Core subjects MUST have class_id
    if payload.type == SubjectType.core and payload.class_id is None:
        raise HTTPException(
            status_code=400,
            detail="Core subjects must be linked to a class",
        )

    subject = Subject(
        name=payload.name,
        type=payload.type,
        class_id=payload.class_id,
        teacher_id=payload.teacher_id,
    )

    db.add(subject)
    await db.flush()

    # AUTO-ENROLL students for CORE subjects
    if payload.type == SubjectType.core:
        result = await db.execute(
            select(User).where(
                User.role == UserRole.student,
                User.class_id == payload.class_id,
            )
        )
        students = result.scalars().all()

        for student in students:
            enrollment = SubjectStudent(
                subject_id=subject.id,
                student_id=student.id,
            )
            db.add(enrollment)

    await db.commit()
    await db.refresh(subject)

    return subject

```

---

### `backend\app\services\sync_service.py`

```python
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


```

---

### `backend\app\services\teacher_ai_service.py`

```python
from app.ai import OllamaClient, select_model
from app.schemas.common import ClientContext

ollama = OllamaClient()


async def suggest_test_questions(
    subject: str,
    difficulty: str,
    context: ClientContext,
) -> dict:
    model = select_model(context)

    prompt = f"""
Suggest exam-quality questions WITH answers.

Subject: {subject}
Difficulty: {difficulty}

Rules:
- Accurate
- Syllabus-aligned
- Teacher will review
"""

    response = await ollama.generate(
        prompt=prompt,
        model_name=model,
        temperature=0.35,
        max_tokens=1000,
    )

    return {"suggestions": response}


async def suggest_assignment_outline(
    subject: str,
    topic: str,
    context: ClientContext,
) -> dict:
    model = select_model(context)

    prompt = f"""
Create an assignment outline for students.

Subject: {subject}
Topic: {topic}

Rules:
- Clear objectives
- Structured tasks
"""

    response = await ollama.generate(
        prompt=prompt,
        model_name=model,
        temperature=0.3,
        max_tokens=800,
    )

    return {"outline": response}

```

---

### `backend\app\services\teacher_assignment_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.assignments import Assignment
from app.schemas.assignments import AssignmentCreateRequest, AssignmentResponse


async def create_assignment(
    payload: AssignmentCreateRequest,
    assignment_type: str,
    db: AsyncSession,
) -> AssignmentResponse:
    assignment = Assignment(
        created_by=1,  # teacher_id (auth wired later)
        title=payload.title,
        subject=payload.subject,
        description=payload.description,
        due_date=payload.due_date,
    )

    # Store assignment type in metadata-like pattern (future-proof)
    assignment.metadata = {
        "assignment_type": assignment_type
    }

    db.add(assignment)
    await db.commit()
    await db.refresh(assignment)

    return AssignmentResponse(
        id=assignment.id,
        title=assignment.title,
        subject=assignment.subject,
        due_date=assignment.due_date,
    )

```

---

### `backend\app\services\teacher_context.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.subject import Subject
from app.models.user import User, UserRole


async def get_teacher_subject(
    teacher_id: int,
    db: AsyncSession,
) -> Subject:
    """
    Returns the subject taught by the teacher.
    Enforces exactly one subject per teacher (current system rule).
    """
    result = await db.execute(
        select(Subject).where(Subject.teacher_id == teacher_id)
    )
    subject = result.scalar_one_or_none()

    if not subject:
        raise HTTPException(
            status_code=403,
            detail="Teacher is not assigned to any subject",
        )

    return subject

```

---

### `backend\app\services\teacher_notes_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.notes import GeneratedNote
from app.schemas.notes import NotesGenerateRequest, NotesResponse
from app.ai import OllamaClient, select_model
from app.services.file_validation import validate_upload
from fastapi import UploadFile, HTTPException
import uuid
import os
from app.models.user import User
ollama = OllamaClient()

UPLOAD_DIR = "app/uploads/teacher_notes"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def create_manual_notes(
    payload: NotesGenerateRequest,
    db: AsyncSession,
) -> NotesResponse:
    """
    Teacher provides full content manually.
    """

    note = GeneratedNote(
        user_id=1,  # replaced by auth later
        subject=payload.subject,
        chapter=payload.chapter,
        difficulty=payload.difficulty,
        pdf_url="",
        extra_data={
            "mode": "manual",
            "content": payload.context.get("manual_content", ""),
        },
    )

    db.add(note)
    await db.commit()
    await db.refresh(note)

    return NotesResponse(
        content_id=str(note.id),
        summary="Manual notes created",
        pdf_url=None,
        offline_ready=False,
        expires_at=None,
    )


async def generate_teacher_notes(
    payload,
    db: AsyncSession,
    current_user: User,
):
    raw_content = payload.raw_ai_output

    if not raw_content or not raw_content.strip():
        raise HTTPException(status_code=400, detail="AI returned empty content")

    note = GeneratedNote(
        user_id=current_user.id,
        subject=payload.subject,
        chapter=payload.chapter,
        difficulty=payload.difficulty,
        content=raw_content,
        is_student_generated=False,
        is_teacher_provided=True,
    )

    db.add(note)
    await db.commit()
    await db.refresh(note)

    return note


async def upload_notes_file(
    subject: str,
    chapter: str,
    file: UploadFile,
    db: AsyncSession,
) -> NotesResponse:
    """
    Upload teacher-created PDF notes.
    """

    await validate_upload(file)

    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    note = GeneratedNote(
        user_id=1,  # replaced by auth later
        subject=subject,
        chapter=chapter,
        difficulty="custom",
        pdf_url=path,
        is_student_generated=False,
        is_teacher_provided=True,
        extra_data={
            "mode": "upload",
            "original_filename": file.filename,
        },
    )

    db.add(note)
    await db.commit()
    await db.refresh(note)

    return NotesResponse(
        content_id=str(note.id),
        summary="Uploaded notes",
        pdf_url=path,
        offline_ready=True,
        expires_at=None,
    )

```

---

### `backend\app\services\teacher_report_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.progress import Progress
from app.models.test import Test
from app.models.assignments import Assignment


async def get_student_report(
    student_id: int,
    db: AsyncSession,
) -> dict:
    progress = await db.execute(
        select(Progress).where(Progress.user_id == student_id)
    )
    progress = progress.scalar_one_or_none()

    tests = await db.execute(
        select(Test).where(Test.created_by == student_id)
    )
    assignments = await db.execute(
        select(Assignment).where(Assignment.created_by == student_id)
    )

    return {
        "student_id": student_id,
        "progress": progress,
        "tests_attempted": tests.scalars().all(),
        "assignments": assignments.scalars().all(),
    }

```

---

### `backend\app\services\teacher_student_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.subject import SubjectType
from app.models.subject_student import SubjectStudent
from app.models.user import User, UserRole


async def get_students_for_subject(
    subject,
    db: AsyncSession,
):
    """
    Returns students visible to the teacher based on subject type.
    """

    # CORE SUBJECT → all students in the class
    if subject.type == SubjectType.core:
        result = await db.execute(
            select(User).where(
                User.role == UserRole.student,
                User.class_id == subject.class_id,
            )
        )
        return result.scalars().all()

    # ELECTIVE SUBJECT → only enrolled students
    result = await db.execute(
        select(User)
        .join(SubjectStudent, SubjectStudent.student_id == User.id)
        .where(SubjectStudent.subject_id == subject.id)
    )
    return result.scalars().all()

```

---

### `backend\app\services\teacher_test_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.test import Test
from app.schemas.tests import TestCreateRequest, TestResponse
from app.ai import OllamaClient
from app.security import get_current_user
from app.models.user import User
from app.models.test_question import TestQuestion

from sqlalchemy import select
from fastapi import HTTPException
from app.models.subject import Subject

import json
from fastapi import Depends
import re

ollama = OllamaClient()


async def create_test_manual(
    payload: TestCreateRequest,
    db: AsyncSession,
    current_user: User =Depends(get_current_user),
) -> TestResponse:
    test = Test(
        created_by=current_user.id,  # teacher_id
        title=payload.title,
        subject=payload.subject,
        difficulty=payload.difficulty,
        questions=[],  # manually provided later
        total_marks=100,
    )

    db.add(test)
    await db.commit()
    await db.refresh(test)

    return TestResponse(
        test_id=test.id,
        title=test.title,
        total_marks=test.total_marks,
    )

def parse_ai_json_safely(raw: str):
    """
    Extracts and parses JSON array from LLM output.
    Preserves LaTeX/KaTeX content.
    """

    raw = raw.strip()

    # Remove markdown fences
    raw = re.sub(r"^```(?:json)?", "", raw)
    raw = re.sub(r"```$", "", raw)

    # Extract JSON array
    start = raw.find("[")
    end = raw.rfind("]")

    if start == -1 or end == -1:
        raise ValueError("AI did not return a valid JSON array.")

    candidate = raw[start:end + 1]

    try:
        return json.loads(candidate)
    except json.JSONDecodeError as e:
        print("AI RAW OUTPUT:\n", candidate)
        raise ValueError(f"Malformed AI JSON: {e}")


async def create_test_ai_assisted(
    payload,
    db: AsyncSession,
    current_user: User,
):
    # 🔹 1. Validate subject_id
    result = await db.execute(
        select(Subject).where(Subject.id == payload.subject_id)
    )
    subject = result.scalar_one_or_none()

    if not subject:
        raise HTTPException(status_code=400, detail="Invalid subject_id")

    # 🔹 2. Build AI prompt using REAL fields
    prompt = f"""
Generate multiple choice questions for:

Subject: {payload.subject}
Chapter: {payload.chapter}
Difficulty: {payload.difficulty}

Return ONLY valid JSON in this format:

[
  {{
    "question": "...",
    "options": ["A", "B", "C", "D"],
    "correct_answer": "..."
  }}
]

Ensure valid JSON. Escape inner quotes properly.
"""

    # 🔹 3. Call AI
    raw = await ollama.generate(
        model_name="mistral:7b-instruct",
        prompt=prompt,
        temperature=0.3,
        max_tokens=1200,
    )

    questions_data = parse_ai_json_safely(raw)

    if not isinstance(questions_data, list) or len(questions_data) == 0:
        raise HTTPException(status_code=400, detail="AI returned invalid questions")

    # 🔹 4. Create Test
    test = Test(
        title=payload.title,
        subject_id=payload.subject_id,
        created_by_student_id=current_user.id,
        difficulty=payload.difficulty,
        total_questions=len(questions_data),
    )

    db.add(test)
    await db.flush()

    # 🔹 5. Insert TestQuestion rows
    for index, q in enumerate(questions_data):
        if (
            "question" not in q
            or "options" not in q
            or "correct_answer" not in q
        ):
            raise HTTPException(status_code=400, detail="Malformed AI question")

        question_row = TestQuestion(
            test_id=test.id,
            question_text=q["question"],   # KaTeX preserved
            options=q["options"],
            correct_answer=q["correct_answer"],
            question_order=index,
        )

        db.add(question_row)

    await db.commit()
    await db.refresh(test)

    return test
```

---

### `backend\app\services\test_evaluation_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.test import Test
from app.models.test_question import TestQuestion
from app.models.test_attempt import TestAttempt
from app.models.test_answer import TestAnswer
from app.models.user import User
from app.services.xp_service import apply_xp_event


async def evaluate_test_submission(
    test_id: int,
    submitted_answers: list[dict],
    db: AsyncSession,
    current_user: User,
):
    result = await db.execute(
        select(Test).where(Test.id == test_id)
    )
    test = result.scalar_one_or_none()

    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    result = await db.execute(
        select(TestQuestion).where(TestQuestion.test_id == test_id)
    )
    questions = result.scalars().all()

    if not questions:
        raise HTTPException(status_code=400, detail="No questions found")

    # Ensure stable order
    questions = sorted(questions, key=lambda q: q.question_order)

    question_map = {q.id: q for q in questions}

    attempt = TestAttempt(
        test_id=test_id,
        student_id=current_user.id,
        score=0,
        percentage=0.0,
    )

    db.add(attempt)
    await db.flush()

    correct_count = 0
    results = []

    for submission in submitted_answers:
        qid = submission.question_id
        selected = submission.selected_answer

        if qid not in question_map:
            raise HTTPException(status_code=400, detail="Invalid question")

        question = question_map[qid]
        is_correct = selected == question.correct_answer

        if is_correct:
            correct_count += 1

        db.add(
            TestAnswer(
                test_attempt_id=attempt.id,
                question_id=qid,
                selected_answer=selected,
                is_correct=is_correct,
            )
        )

        # Build result entry
        question_index = questions.index(question)

        results.append({
            "question_index": question_index,
            "is_correct": is_correct,
            "correct_answer": question.correct_answer,
        })

    total = len(questions)
    percentage = (correct_count / total) * 100 if total else 0

    attempt.score = correct_count
    attempt.percentage = percentage
    xp_awarded = 100
    await db.flush()
    await apply_xp_event(
        user_id=current_user.id,
        event="TEST_COMPLETED",
        db=db,
    )

    await db.commit()

    return {
        "score": correct_count,
        "total_questions": total,
        "percentage": round(percentage, 2),
        "xp_awarded": xp_awarded,
        "results": results,
    }


```

---

### `backend\app\services\test_service.py`

```python
from app.ai import OllamaClient
from app.schemas.tests import TestCreateRequest, TestResponse

ollama = OllamaClient()


async def generate_test(request: TestCreateRequest) -> TestResponse:
    prompt = f"""
Create an exam-style test.

Subject: {request.subject}
Difficulty: {request.difficulty}

Rules:
- Multiple choice
- One correct answer
- Clear options
"""

    response = await ollama.generate(
        prompt=prompt,
        model_name="mistral:7b-instruct",
        temperature=0.4,
        max_tokens=1500,
    )

    return TestResponse(
        test_id=1,
        title=request.title,
        total_marks=100,
    )

```

---

### `backend\app\services\xp_service.py`

```python
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


```

---

### `backend\app\utils\ai_client.py`

```python
# backend/app/utils/ai_client.py

import json
import re
import os
from typing import Any, Dict
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=api_key)


# ============================================================
# 1. FUNCTION CALLING SUPPORT (CORRECT FOR CHAT COMPLETIONS)
# ============================================================

async def call_json_function(model: str, messages: list, function_schema: dict) -> Dict[str, Any]:
    """
    Calls OpenAI chat.completions.create() using function-calling
    and returns the parsed JSON arguments.
    """

    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        tools=[{
            "type": "function",
            "function": function_schema
        }],
        tool_choice={"type": "function", "function": {"name": function_schema["name"]}},
        temperature=0.2
    )

    try:
        # Correct extraction for ChatCompletionMessageFunctionToolCall
        tool_call = response.choices[0].message.tool_calls[0]
        args_str = tool_call.function.arguments  # <-- this is a string
        return json.loads(args_str)

    except Exception as e:
        raise ValueError(
            f"Function call JSON parse failed: {e}\n"
            f"Raw: {response}"
        )


# ============================================================
# 2. FLASHCARD LEGACY SUPPORT (UNCHANGED)
# ============================================================

def _extract_text_from_response(response: Any) -> str:
    try:
        return response.choices[0].message.content
    except Exception:
        return ""


def _strip_code_fences(text: str) -> str:
    cleaned = re.sub(r"^```(?:json)?\s*", "", text)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def _extract_first_json(text: str) -> str:
    start = text.find("{")
    if start == -1:
        raise ValueError("No JSON found in AI output.")
    for end in range(len(text) - 1, start, -1):
        try:
            json.loads(text[start:end])
            return text[start:end]
        except:
            pass
    raise ValueError("Unable to extract JSON from AI output.")


async def generate_flashcard_ai_output(subject: str, chapter: str, max_cards: int = 20) -> Dict[str, Any]:
    """
    Legacy flashcard generator — kept EXACTLY as your flashcards expect.
    """

    prompt = f"""
Generate up to {max_cards} flashcards for subject '{subject}' and chapter '{chapter}'.

Respond ONLY with valid JSON in this format:

{{
    "cards": [
        {{
            "front": "Question text",
            "back": "Answer text"
        }}
    ]
}}
"""

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a flashcard generator that outputs ONLY valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    text = _extract_text_from_response(response)
    if not text:
        raise ValueError("AI returned empty response.")

    cleaned = _strip_code_fences(text)

    try:
        return json.loads(cleaned)
    except:
        candidate = _extract_first_json(cleaned)
        return json.loads(candidate)

```

---

### `backend\app\utils\sanitize.py`

```python
import re


def sanitize_markdown(md: str) -> str:
    # Basic sanitization to avoid unsupported chars
    if not md:
        return ""
    # Replace some unicode chars that fpdf may struggle with
    replacements = {
        "\u2013": "-",  # en dash
        "\u2014": "-",  # em dash
        "\u2022": "-",  # bullet
        "\u00b2": "^2",  # superscript 2
    }
    for k, v in replacements.items():
        md = md.replace(k, v)
    # Trim repeated blank lines
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()

```
