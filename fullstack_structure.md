# Full Stack Project Structure

## Backend Folder Structure

```
├── app/
│   ├── __init__.py
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── model_router.py
│   │   └── ollama_client.py
│   ├── config.py
│   ├── db/
│   │   ├── base.py
│   │   ├── base_imports.py
│   │   ├── init_db.py
│   │   └── session.py
│   ├── logging/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   └── middleware.py
│   ├── loop_fix.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── assignments.py
│   │   ├── classroom.py
│   │   ├── flashcards.py
│   │   ├── notes.py
│   │   ├── progress.py
│   │   ├── subject.py
│   │   ├── subject_student.py
│   │   ├── tests.py
│   │   ├── user.py
│   │   └── users.py
│   ├── pdfs/
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── context_builder.py
│   │   ├── guardrails.py
│   │   └── retriever.py
│   ├── repositories/
│   │   ├── assignment_repo.py
│   │   ├── base_repo.py
│   │   ├── flashcard_repo.py
│   │   └── note_repo.py
│   ├── routers/
│   │   ├── admin/
│   │   │   ├── __init__.py
│   │   │   ├── _guards.py
│   │   │   ├── content.py
│   │   │   ├── system.py
│   │   │   └── users.py
│   │   ├── auth.py
│   │   ├── parent/
│   │   │   ├── __init__.py
│   │   │   ├── _guards.py
│   │   │   ├── insights.py
│   │   │   ├── overview.py
│   │   │   └── progress.py
│   │   ├── student/
│   │   │   ├── __init__.py
│   │   │   ├── _guards.py
│   │   │   ├── ai_chat.py
│   │   │   ├── assignments.py
│   │   │   ├── flashcards.py
│   │   │   ├── notes.py
│   │   │   ├── progress.py
│   │   │   ├── sync.py
│   │   │   ├── teacher_notes.py
│   │   │   └── tests.py
│   │   ├── subjects.py
│   │   └── teacher/
│   │       ├── __init__.py
│   │       ├── _guards.py
│   │       ├── ai_tools.py
│   │       ├── assignments.py
│   │       ├── notes.py
│   │       ├── reports.py
│   │       ├── students.py
│   │       └── tests.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── assignments.py
│   │   ├── auth.py
│   │   ├── common.py
│   │   ├── flashcards.py
│   │   ├── notes.py
│   │   ├── progress.py
│   │   ├── subject.py
│   │   ├── sync.py
│   │   ├── tests.py
│   │   └── user.py
│   ├── security/
│   │   ├── __init__.py
│   │   ├── admin_guard.py
│   │   ├── dependencies.py
│   │   ├── guards.py
│   │   ├── oauth2.py
│   │   ├── passwords.py
│   │   ├── rate_limiter.py
│   │   └── roles.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── admin_system_service.py
│   │   ├── admin_user_service.py
│   │   ├── ai_service.py
│   │   ├── auth_service.py
│   │   ├── elective_enrollment_service.py
│   │   ├── enrollment_guard.py
│   │   ├── file_validation.py
│   │   ├── flashcards_service.py
│   │   ├── notes_service.py
│   │   ├── parent_insights_service.py
│   │   ├── parent_overview_service.py
│   │   ├── pdf_generator.py
│   │   ├── subject_service.py
│   │   ├── sync_service.py
│   │   ├── teacher_ai_service.py
│   │   ├── teacher_assignment_service.py
│   │   ├── teacher_context.py
│   │   ├── teacher_notes_service.py
│   │   ├── teacher_report_service.py
│   │   ├── teacher_student_service.py
│   │   ├── teacher_test_service.py
│   │   ├── test_service.py
│   │   └── xp_service.py
│   ├── uploads/
│   │   └── teacher_notes/
│   ├── utils/
│   │   ├── ai_client.py
│   │   └── sanitize.py
│   └── vector/
├── app.py
├── templates/
│   ├── index.html
│   └── notes_template.html
├── test_loop.py
├── test_token.py
└── worker/
    ├── jobs/
    │   ├── generate_notes_pdf.py
    │   └── worker.py
    └── queue.py
```

## Backend Code Imports Overview

### backend\app.py
```python
import os, re
from io import BytesIO
from flask import Flask, render_template, request, send_file, jsonify
from dotenv import load_dotenv
from openai import OpenAI
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.units import inch
```

### backend\test_loop.py
```python
import asyncio
```

### backend\test_token.py
```python
import secrets
```

### backend\app\config.py
```python
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
```

### backend\app\loop_fix.py
```python
import asyncio
import sys
```

### backend\app\main.py
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.config import get_settings
from app.logging.middleware import logging_middleware
from app.routers import auth
from app.routers import subjects
from app.routers.student import (
from app.routers.teacher import (
from app.routers.parent import (
from app.routers.admin import (
```

### backend\app\__init__.py
_No imports detected_

### backend\app\ai\model_router.py
```python
from app.schemas.common import ClientContext
from app.config import get_settings
```

### backend\app\ai\ollama_client.py
```python
import httpx
from typing import Dict, Any
from app.config import get_settings
```

### backend\app\ai\__init__.py
```python
from app.ai.ollama_client import OllamaClient
from app.ai.model_router import select_model
```

### backend\app\db\base.py
```python
from sqlalchemy.orm import declarative_base
```

### backend\app\db\base_imports.py
```python
from app.models.user import User
from app.models.progress import Progress
from app.models.classroom import Classroom
from app.models.subject import Subject
from app.models.subject_student import SubjectStudent
```

### backend\app\db\init_db.py
```python
import asyncio
from app.db.session import engine
from app.db.base import Base
import app.db.base_imports  # IMPORTANT
```

### backend\app\db\session.py
```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings
```

### backend\app\logging\logger.py
```python
from loguru import logger
import sys
```

### backend\app\logging\middleware.py
```python
from fastapi import Request
from app.logging.logger import logger
import time
```

### backend\app\logging\__init__.py
```python
from app.logging.logger import logger
from app.logging.middleware import logging_middleware
```

### backend\app\models\assignments.py
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.db.session import Base
```

### backend\app\models\classroom.py
```python
from sqlalchemy import Column, Integer, String
from app.db.base import Base
```

### backend\app\models\flashcards.py
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.session import Base
```

### backend\app\models\notes.py
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.session import Base
```

### backend\app\models\progress.py
```python
from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base
```

### backend\app\models\subject.py
```python
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.db.base import Base
```

### backend\app\models\subject_student.py
```python
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.db.base import Base
```

### backend\app\models\tests.py
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.session import Base
```

### backend\app\models\user.py
```python
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum
```

### backend\app\models\users.py
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.session import Base
```

### backend\app\models\__init__.py
```python
from app.models.users import User
from app.models.notes import GeneratedNote
from app.models.tests import Test
from app.models.assignments import Assignment
from app.models.flashcards import FlashcardSet
from app.models.progress import Progress
```

### backend\app\rag\context_builder.py
```python
from typing import List
```

### backend\app\rag\guardrails.py
_No imports detected_

### backend\app\rag\retriever.py
```python
from typing import List
```

### backend\app\rag\__init__.py
```python
from app.rag.context_builder import build_context
from app.rag.retriever import VectorRetriever
from app.rag.guardrails import validate_context
```

### backend\app\repositories\assignment_repo.py
```python
from ..models.assignments import Assignment
from .base_repo import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession
```

### backend\app\repositories\base_repo.py
```python
from typing import Generic, TypeVar, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import as_declarative
```

### backend\app\repositories\flashcard_repo.py
```python
from ..models.flashcards import FlashcardSet
from .base_repo import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession
import json
```

### backend\app\repositories\note_repo.py
```python
from ..models.notes import Note
from .base_repo import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession
```

### backend\app\routers\auth.py
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.auth import SignupRequest, LoginRequest, AuthResponse
from app.services.auth_service import signup_user, login_user
```

### backend\app\routers\subjects.py
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.subject import SubjectCreateRequest, SubjectResponse
from app.services.subject_service import create_subject
from app.security.dependencies import require_role
from app.models.user import UserRole
```

### backend\app\routers\admin\content.py
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.assignments import Assignment
from app.models.tests import Test
```

### backend\app\routers\admin\system.py
```python
from fastapi import APIRouter
from app.config import get_settings
```

### backend\app\routers\admin\users.py
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.admin_user_service import (
```

### backend\app\routers\admin\_guards.py
```python
from fastapi import Depends
from app.security import require_role
from app.security.roles import Role
```

### backend\app\routers\admin\__init__.py
```python
from app.routers.admin.users import router as users_router
from app.routers.admin.content import router as content_router
from app.routers.admin.system import router as system_router
```

### backend\app\routers\parent\insights.py
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.parent_insights_service import get_parent_insights
```

### backend\app\routers\parent\overview.py
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.parent_overview_service import get_parent_overview
```

### backend\app\routers\parent\progress.py
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.parent_overview_service import get_detailed_progress
```

### backend\app\routers\parent\_guards.py
```python
from fastapi import Depends
from app.security import require_role
from app.security.roles import Role
```

### backend\app\routers\parent\__init__.py
```python
from app.routers.parent.overview import router as overview_router
from app.routers.parent.progress import router as progress_router
from app.routers.parent.insights import router as insights_router
```

### backend\app\routers\student\ai_chat.py
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers.student._guards import student_guard
from app.db.session import get_db
from app.schemas.common import ClientContext
from app.services.ai_service import chat_with_ai
from app.services.xp_service import apply_xp_event
```

### backend\app\routers\student\assignments.py
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ...db.session import get_db
from ...repositories.assignment_repo import AssignmentRepo
from ...schemas.assignments import AssignmentOut
from app.routers.student._guards import student_guard
```

### backend\app\routers\student\flashcards.py
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.common import ClientContext
from app.services.flashcards_service import generate_flashcards
from app.services.xp_service import apply_xp_event
from app.routers.student._guards import student_guard
```

### backend\app\routers\student\notes.py
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.notes import NotesGenerateRequest, NotesResponse
from app.services.notes_service import generate_notes
from app.services.xp_service import apply_xp_event
from app.routers.student._guards import student_guard
```

### backend\app\routers\student\progress.py
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.progress import Progress
from app.routers.student._guards import student_guard
```

### backend\app\routers\student\sync.py
```python
from fastapi import APIRouter
from app.schemas.sync import SyncRequest, SyncResponse
from app.services.sync_service import get_available_sync_items
from app.routers.student._guards import student_guard
```

### backend\app\routers\student\teacher_notes.py
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.routers.student._guards import student_guard
from app.models.notes import GeneratedNote
```

### backend\app\routers\student\tests.py
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers.student._guards import student_guard
from app.db.session import get_db
from app.schemas.tests import TestCreateRequest, TestResponse
from app.services.test_service import generate_test
from app.services.xp_service import apply_xp_event
```

### backend\app\routers\student\_guards.py
```python
from fastapi import Depends
from app.security import require_role
from app.security.roles import Role
```

### backend\app\routers\student\__init__.py
```python
from app.routers.student.notes import router as notes_router
from app.routers.student.flashcards import router as flashcards_router
from app.routers.student.tests import router as tests_router
from app.routers.student.ai_chat import router as ai_chat_router
from app.routers.student.progress import router as progress_router
from app.routers.student.sync import router as sync_router
from app.routers.student.teacher_notes import router as teacher_notes_router
```

### backend\app\routers\teacher\ai_tools.py
```python
from fastapi import APIRouter
from app.schemas.common import ClientContext
from app.services.teacher_ai_service import (
from app.routers.teacher._guards import teacher_guard
```

### backend\app\routers\teacher\assignments.py
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal
from app.db.session import get_db
from app.schemas.assignments import AssignmentCreateRequest, AssignmentResponse
from app.services.teacher_assignment_service import create_assignment
from app.routers.teacher._guards import teacher_guard
```

### backend\app\routers\teacher\notes.py
```python
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal
from app.db.session import get_db
from app.routers.teacher._guards import teacher_guard
from app.schemas.notes import NotesGenerateRequest, NotesResponse
from app.services.teacher_notes_service import (
```

### backend\app\routers\teacher\reports.py
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.teacher_report_service import get_student_report
from app.routers.teacher._guards import teacher_guard
```

### backend\app\routers\teacher\students.py
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.security.dependencies import require_role, get_current_user
from app.models.user import UserRole
from app.services.teacher_context import get_teacher_subject
from app.services.teacher_student_service import get_students_for_subject
```

### backend\app\routers\teacher\tests.py
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal
from app.db.session import get_db
from app.schemas.tests import TestCreateRequest, TestResponse
from app.services.teacher_test_service import (
from app.routers.teacher._guards import teacher_guard
```

### backend\app\routers\teacher\_guards.py
```python
from fastapi import Depends
from app.security import require_role
from app.security.roles import Role
```

### backend\app\routers\teacher\__init__.py
```python
from app.routers.teacher.assignments import router as assignments_router
from app.routers.teacher.tests import router as tests_router
from app.routers.teacher.ai_tools import router as ai_tools_router
from app.routers.teacher.reports import router as reports_router
from app.routers.teacher.notes import router as notes_router
```

### backend\app\schemas\assignments.py
```python
from pydantic import BaseModel
from datetime import datetime
from typing import Literal, Optional
```

### backend\app\schemas\auth.py
```python
from pydantic import BaseModel, EmailStr
from typing import Optional
```

### backend\app\schemas\common.py
```python
from pydantic import BaseModel
from typing import Literal, Optional
```

### backend\app\schemas\flashcards.py
```python
from pydantic import BaseModel
from typing import List
```

### backend\app\schemas\notes.py
```python
from pydantic import BaseModel
from typing import Optional
from app.schemas.common import ClientContext
```

### backend\app\schemas\progress.py
```python
from pydantic import BaseModel
```

### backend\app\schemas\subject.py
```python
from pydantic import BaseModel
from typing import Optional
from enum import Enum
```

### backend\app\schemas\sync.py
```python
from pydantic import BaseModel
from typing import List, Optional
```

### backend\app\schemas\tests.py
```python
from pydantic import BaseModel
from typing import List
```

### backend\app\schemas\user.py
```python
from pydantic import BaseModel
```

### backend\app\schemas\__init__.py
```python
from app.schemas.common import ClientContext
from app.schemas.user import UserResponse
from app.schemas.notes import NotesGenerateRequest, NotesResponse
from app.schemas.tests import TestCreateRequest, TestResponse
from app.schemas.assignments import AssignmentCreateRequest, AssignmentResponse
from app.schemas.flashcards import FlashcardSetResponse
from app.schemas.progress import ProgressResponse
```

### backend\app\security\admin_guard.py
```python
from fastapi import HTTPException, status
```

### backend\app\security\dependencies.py
```python
from fastapi import Depends, HTTPException, status
from app.security.roles import Role
```

### backend\app\security\guards.py
```python
from fastapi import HTTPException
from app.schemas.common import ClientContext
```

### backend\app\security\oauth2.py
```python
from fastapi.security import OAuth2PasswordBearer
```

### backend\app\security\passwords.py
```python
from passlib.context import CryptContext
```

### backend\app\security\rate_limiter.py
```python
import time
from fastapi import HTTPException, Request
```

### backend\app\security\roles.py
```python
from enum import Enum
```

### backend\app\security\__init__.py
```python
from app.security.guards import enforce_client_capabilities
from app.security.rate_limiter import rate_limit
from app.security.admin_guard import require_admin
from app.security.roles import Role
from app.security.dependencies import get_current_user, require_role
```

### backend\app\services\admin_system_service.py
```python
from app.config import get_settings
```

### backend\app\services\admin_user_service.py
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.users import User
```

### backend\app\services\ai_service.py
```python
from typing import List, Dict
from app.ai import OllamaClient, select_model
from app.schemas.common import ClientContext
```

### backend\app\services\auth_service.py
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.user import User, UserRole
from app.models.classroom import Classroom
from app.models.progress import Progress
from app.schemas.auth import SignupRequest, LoginRequest
from app.security.passwords import hash_password, verify_password
```

### backend\app\services\elective_enrollment_service.py
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.subject import Subject
from app.models.subject_student import SubjectStudent
from app.services.enrollment_guard import validate_enrollment_allowed
```

### backend\app\services\enrollment_guard.py
```python
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.subject import Subject, SubjectType
from app.models.subject_student import SubjectStudent
```

### backend\app\services\file_validation.py
```python
from fastapi import UploadFile, HTTPException
```

### backend\app\services\flashcards_service.py
```python
from app.ai import OllamaClient, select_model
from app.schemas.flashcards import FlashcardSetResponse
from app.schemas.common import ClientContext
```

### backend\app\services\notes_service.py
```python
from app.ai import OllamaClient, select_model
from app.schemas.notes import NotesGenerateRequest, NotesResponse
from app.rag import build_context, validate_context
from sqlalchemy.ext.asyncio import AsyncSession
```

### backend\app\services\parent_insights_service.py
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.progress import Progress
from app.ai import OllamaClient
```

### backend\app\services\parent_overview_service.py
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.progress import Progress
from app.models.assignments import Assignment
from app.models.tests import Test
```

### backend\app\services\pdf_generator.py
```python
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT
```

### backend\app\services\subject_service.py
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.subject import Subject, SubjectType
from app.models.subject_student import SubjectStudent
from app.models.user import User, UserRole
from app.schemas.subject import SubjectCreateRequest
```

### backend\app\services\sync_service.py
```python
from typing import List
from datetime import datetime
from app.schemas.sync import SyncItem, SyncResponse
```

### backend\app\services\teacher_ai_service.py
```python
from app.ai import OllamaClient, select_model
from app.schemas.common import ClientContext
```

### backend\app\services\teacher_assignment_service.py
```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.assignments import Assignment
from app.schemas.assignments import AssignmentCreateRequest, AssignmentResponse
```

### backend\app\services\teacher_context.py
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.subject import Subject
from app.models.user import User, UserRole
```

### backend\app\services\teacher_notes_service.py
```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.notes import GeneratedNote
from app.schemas.notes import NotesGenerateRequest, NotesResponse
from app.ai import OllamaClient, select_model
from app.services.file_validation import validate_upload
from fastapi import UploadFile
import uuid
import os
```

### backend\app\services\teacher_report_service.py
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.progress import Progress
from app.models.tests import Test
from app.models.assignments import Assignment
```

### backend\app\services\teacher_student_service.py
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.subject import SubjectType
from app.models.subject_student import SubjectStudent
from app.models.user import User, UserRole
```

### backend\app\services\teacher_test_service.py
```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tests import Test
from app.schemas.tests import TestCreateRequest, TestResponse
from app.ai import OllamaClient
```

### backend\app\services\test_service.py
```python
from app.ai import OllamaClient
from app.schemas.tests import TestCreateRequest, TestResponse
```

### backend\app\services\xp_service.py
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.progress import Progress
```

### backend\app\services\__init__.py
```python
from app.services.notes_service import generate_notes
from app.services.flashcards_service import generate_flashcards
from app.services.test_service import generate_test
from app.services.ai_service import chat_with_ai
from app.services.xp_service import apply_xp_event
from app.services.teacher_assignment_service import create_assignment
from app.services.teacher_test_service import (
from app.services.teacher_ai_service import (
from app.services.teacher_report_service import get_student_report
from app.services.parent_overview_service import (
from app.services.parent_insights_service import get_parent_insights
from app.services.admin_user_service import (
from app.services.admin_system_service import get_system_status
from app.services.teacher_notes_service import (
from app.services.file_validation import validate_upload
```

### backend\app\utils\ai_client.py
```python
import json
import re
import os
from typing import Any, Dict
from openai import AsyncOpenAI
from dotenv import load_dotenv
```

### backend\app\utils\sanitize.py
```python
import re
```

### backend\templates\index.html
_No imports detected_

### backend\templates\notes_template.html
_No imports detected_

### backend\worker\queue.py
```python
import os
from redis import Redis
from rq import Queue
```

### backend\worker\jobs\generate_notes_pdf.py
```python
from app.services.notes_service import generate_notes
from app.services.pdf_generator import generate_notes_pdf
```

### backend\worker\jobs\worker.py
```python
import os
from redis import Redis
from rq import Worker, Connection
from worker.queue import default_queue, pdf_queue, ai_queue
```

## Frontend Folder Structure

```
├── README.md
├── components.json
├── eslint.config.js
├── index.html
├── package-lock.json
├── package.json
├── postcss.config.js
├── public/
├── src/
│   ├── App.css
│   ├── App.tsx
│   ├── components/
│   │   ├── MarkdownKatexRenderer.tsx
│   │   ├── NavLink.tsx
│   │   ├── auth/
│   │   │   └── ProtectedRoute.tsx
│   │   ├── cards/
│   │   │   ├── ActionCard.tsx
│   │   │   ├── RoleCard.tsx
│   │   │   └── StatCard.tsx
│   │   ├── gamification/
│   │   │   ├── LevelBadge.tsx
│   │   │   ├── StreakIndicator.tsx
│   │   │   ├── XPBadge.tsx
│   │   │   ├── XPBar.tsx
│   │   │   └── XPGainAnimation.tsx
│   │   ├── layout/
│   │   │   ├── OfflineBanner.tsx
│   │   │   └── StudentHeader.tsx
│   │   ├── progress/
│   │   │   └── ProgressRing.tsx
│   │   ├── timeline/
│   │   │   └── AcademicTimeline.tsx
│   │   └── ui/
│   │       ├── accordion.tsx
│   │       ├── alert-dialog.tsx
│   │       ├── alert.tsx
│   │       ├── aspect-ratio.tsx
│   │       ├── avatar.tsx
│   │       ├── badge.tsx
│   │       ├── breadcrumb.tsx
│   │       ├── button.tsx
│   │       ├── calendar.tsx
│   │       ├── card.tsx
│   │       ├── carousel.tsx
│   │       ├── chart.tsx
│   │       ├── checkbox.tsx
│   │       ├── collapsible.tsx
│   │       ├── command.tsx
│   │       ├── context-menu.tsx
│   │       ├── dialog.tsx
│   │       ├── drawer.tsx
│   │       ├── dropdown-menu.tsx
│   │       ├── form.tsx
│   │       ├── hover-card.tsx
│   │       ├── input-otp.tsx
│   │       ├── input.tsx
│   │       ├── label.tsx
│   │       ├── menubar.tsx
│   │       ├── navigation-menu.tsx
│   │       ├── pagination.tsx
│   │       ├── popover.tsx
│   │       ├── progress.tsx
│   │       ├── radio-group.tsx
│   │       ├── resizable.tsx
│   │       ├── scroll-area.tsx
│   │       ├── select.tsx
│   │       ├── separator.tsx
│   │       ├── sheet.tsx
│   │       ├── sidebar.tsx
│   │       ├── skeleton.tsx
│   │       ├── slider.tsx
│   │       ├── sonner.tsx
│   │       ├── switch.tsx
│   │       ├── table.tsx
│   │       ├── tabs.tsx
│   │       ├── textarea.tsx
│   │       ├── toast.tsx
│   │       ├── toaster.tsx
│   │       ├── toggle-group.tsx
│   │       ├── toggle.tsx
│   │       ├── tooltip.tsx
│   │       └── use-toast.ts
│   ├── contexts/
│   │   ├── AuthContext.tsx
│   │   └── OnlineContext.tsx
│   ├── hooks/
│   │   ├── use-mobile.tsx
│   │   └── use-toast.ts
│   ├── index.css
│   ├── lib/
│   │   └── utils.ts
│   ├── main.tsx
│   ├── pages/
│   │   ├── Index.tsx
│   │   ├── NotFound.tsx
│   │   ├── RoleSelection.tsx
│   │   ├── auth/
│   │   │   ├── LoginPage.tsx
│   │   │   └── SignupPage.tsx
│   │   ├── parent/
│   │   │   └── ParentDashboard.tsx
│   │   ├── student/
│   │   │   ├── AssignmentsPage.tsx
│   │   │   ├── DoubtChatPage.tsx
│   │   │   ├── FlashcardsPage.tsx
│   │   │   ├── NotesPage.tsx
│   │   │   ├── StudentDashboard.tsx
│   │   │   ├── TestsPage.tsx
│   │   │   └── WatchVideosPage.tsx
│   │   └── teacher/
│   │       ├── AIContentPage.tsx
│   │       ├── AnalyticsPage.tsx
│   │       ├── CreateAssignmentPage.tsx
│   │       ├── CreateTestPage.tsx
│   │       ├── SubmissionsPage.tsx
│   │       └── TeacherDashboard.tsx
│   └── vite-env.d.ts
├── tailwind.config.ts
├── tsconfig.app.json
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts
```

## Frontend Code Imports Overview

### frontend\bildofy-lms-lovable\components.json
_No imports detected_

### frontend\bildofy-lms-lovable\eslint.config.js
```text
import js from "@eslint/js";
import globals from "globals";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";
import tseslint from "typescript-eslint";
```

### frontend\bildofy-lms-lovable\index.html
_No imports detected_

### frontend\bildofy-lms-lovable\package-lock.json
_No imports detected_

### frontend\bildofy-lms-lovable\package.json
_No imports detected_

### frontend\bildofy-lms-lovable\postcss.config.js
_No imports detected_

### frontend\bildofy-lms-lovable\README.md
_No imports detected_

### frontend\bildofy-lms-lovable\tailwind.config.ts
```text
import type { Config } from "tailwindcss";
```

### frontend\bildofy-lms-lovable\tsconfig.app.json
_No imports detected_

### frontend\bildofy-lms-lovable\tsconfig.json
_No imports detected_

### frontend\bildofy-lms-lovable\tsconfig.node.json
_No imports detected_

### frontend\bildofy-lms-lovable\vite.config.ts
```text
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";
import { componentTagger } from "lovable-tagger";
```

### frontend\bildofy-lms-lovable\src\App.css
```text
from {
```

### frontend\bildofy-lms-lovable\src\App.tsx
```text
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { OnlineProvider } from "@/contexts/OnlineContext";
import { OfflineBanner } from "@/components/layout/OfflineBanner";
import { AuthProvider, useAuth } from "@/contexts/AuthContext";
import LoginPage from "./pages/auth/LoginPage";
import SignupPage from "./pages/auth/SignupPage";
import StudentDashboard from "./pages/student/StudentDashboard";
import NotesPage from "./pages/student/NotesPage";
import TestsPage from "./pages/student/TestsPage";
import AssignmentsPage from "./pages/student/AssignmentsPage";
import FlashcardsPage from "./pages/student/FlashcardsPage";
```

### frontend\bildofy-lms-lovable\src\index.css
_No imports detected_

### frontend\bildofy-lms-lovable\src\main.tsx
```text
import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import "./index.css";
import 'katex/dist/katex.min.css';
```

### frontend\bildofy-lms-lovable\src\vite-env.d.ts
_No imports detected_

### frontend\bildofy-lms-lovable\src\components\MarkdownKatexRenderer.tsx
```text
import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
```

### frontend\bildofy-lms-lovable\src\components\NavLink.tsx
```text
import { NavLink as RouterNavLink, NavLinkProps } from "react-router-dom";
import { forwardRef } from "react";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\auth\ProtectedRoute.tsx
```text
import { Navigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
```

### frontend\bildofy-lms-lovable\src\components\cards\ActionCard.tsx
```text
import React from 'react';
import { cn } from '@/lib/utils';
import { XPBadge } from '@/components/gamification/XPBadge';
import { useOnlineStatus } from '@/contexts/OnlineContext';
import { LucideIcon, WifiOff, ChevronRight, Check } from 'lucide-react';
```

### frontend\bildofy-lms-lovable\src\components\cards\RoleCard.tsx
```text
import React from 'react';
import { cn } from '@/lib/utils';
import { LucideIcon, ArrowRight } from 'lucide-react';
```

### frontend\bildofy-lms-lovable\src\components\cards\StatCard.tsx
```text
import React from 'react';
import { cn } from '@/lib/utils';
import { LucideIcon, TrendingUp, TrendingDown } from 'lucide-react';
```

### frontend\bildofy-lms-lovable\src\components\gamification\LevelBadge.tsx
```text
import React from 'react';
import { cn } from '@/lib/utils';
import { Star } from 'lucide-react';
```

### frontend\bildofy-lms-lovable\src\components\gamification\StreakIndicator.tsx
```text
import React from 'react';
import { cn } from '@/lib/utils';
import { Flame } from 'lucide-react';
```

### frontend\bildofy-lms-lovable\src\components\gamification\XPBadge.tsx
```text
import React from 'react';
import { cn } from '@/lib/utils';
import { Zap } from 'lucide-react';
```

### frontend\bildofy-lms-lovable\src\components\gamification\XPBar.tsx
```text
import React from 'react';
import { cn } from '@/lib/utils';
import { Sparkles } from 'lucide-react';
```

### frontend\bildofy-lms-lovable\src\components\gamification\XPGainAnimation.tsx
```text
import React, { useEffect, useState } from 'react';
import { cn } from '@/lib/utils';
import { Zap } from 'lucide-react';
```

### frontend\bildofy-lms-lovable\src\components\layout\OfflineBanner.tsx
```text
import React from 'react';
import { useOnlineStatus } from '@/contexts/OnlineContext';
import { WifiOff, CloudOff } from 'lucide-react';
import { cn } from '@/lib/utils';
```

### frontend\bildofy-lms-lovable\src\components\layout\StudentHeader.tsx
```text
import React from 'react';
import { XPBar } from '@/components/gamification/XPBar';
import { StreakIndicator } from '@/components/gamification/StreakIndicator';
import { LevelBadge } from '@/components/gamification/LevelBadge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Bell, Settings, Menu } from 'lucide-react';
import { Link } from 'react-router-dom';
```

### frontend\bildofy-lms-lovable\src\components\progress\ProgressRing.tsx
```text
import React from 'react';
import { cn } from '@/lib/utils';
```

### frontend\bildofy-lms-lovable\src\components\timeline\AcademicTimeline.tsx
```text
import React from 'react';
import { cn } from '@/lib/utils';
import { XPBadge } from '@/components/gamification/XPBadge';
import {
import { format, isToday, isTomorrow, isPast } from 'date-fns';
```

### frontend\bildofy-lms-lovable\src\components\ui\accordion.tsx
```text
import * as React from "react";
import * as AccordionPrimitive from "@radix-ui/react-accordion";
import { ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\alert-dialog.tsx
```text
import * as React from "react";
import * as AlertDialogPrimitive from "@radix-ui/react-alert-dialog";
import { cn } from "@/lib/utils";
import { buttonVariants } from "@/components/ui/button";
```

### frontend\bildofy-lms-lovable\src\components\ui\alert.tsx
```text
import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\aspect-ratio.tsx
```text
import * as AspectRatioPrimitive from "@radix-ui/react-aspect-ratio";
```

### frontend\bildofy-lms-lovable\src\components\ui\avatar.tsx
```text
import * as React from "react";
import * as AvatarPrimitive from "@radix-ui/react-avatar";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\badge.tsx
```text
import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\breadcrumb.tsx
```text
import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { ChevronRight, MoreHorizontal } from "lucide-react";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\button.tsx
```text
import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\calendar.tsx
```text
import * as React from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { DayPicker } from "react-day-picker";
import { cn } from "@/lib/utils";
import { buttonVariants } from "@/components/ui/button";
```

### frontend\bildofy-lms-lovable\src\components\ui\card.tsx
```text
import * as React from "react";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\carousel.tsx
```text
import * as React from "react";
import useEmblaCarousel, { type UseEmblaCarouselType } from "embla-carousel-react";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
```

### frontend\bildofy-lms-lovable\src\components\ui\chart.tsx
```text
import * as React from "react";
import * as RechartsPrimitive from "recharts";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\checkbox.tsx
```text
import * as React from "react";
import * as CheckboxPrimitive from "@radix-ui/react-checkbox";
import { Check } from "lucide-react";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\collapsible.tsx
```text
import * as CollapsiblePrimitive from "@radix-ui/react-collapsible";
```

### frontend\bildofy-lms-lovable\src\components\ui\command.tsx
```text
import * as React from "react";
import { type DialogProps } from "@radix-ui/react-dialog";
import { Command as CommandPrimitive } from "cmdk";
import { Search } from "lucide-react";
import { cn } from "@/lib/utils";
import { Dialog, DialogContent } from "@/components/ui/dialog";
```

### frontend\bildofy-lms-lovable\src\components\ui\context-menu.tsx
```text
import * as React from "react";
import * as ContextMenuPrimitive from "@radix-ui/react-context-menu";
import { Check, ChevronRight, Circle } from "lucide-react";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\dialog.tsx
```text
import * as React from "react";
import * as DialogPrimitive from "@radix-ui/react-dialog";
import { X } from "lucide-react";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\drawer.tsx
```text
import * as React from "react";
import { Drawer as DrawerPrimitive } from "vaul";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\dropdown-menu.tsx
```text
import * as React from "react";
import * as DropdownMenuPrimitive from "@radix-ui/react-dropdown-menu";
import { Check, ChevronRight, Circle } from "lucide-react";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\form.tsx
```text
import * as React from "react";
import * as LabelPrimitive from "@radix-ui/react-label";
import { Slot } from "@radix-ui/react-slot";
import { Controller, ControllerProps, FieldPath, FieldValues, FormProvider, useFormContext } from "react-hook-form";
import { cn } from "@/lib/utils";
import { Label } from "@/components/ui/label";
```

### frontend\bildofy-lms-lovable\src\components\ui\hover-card.tsx
```text
import * as React from "react";
import * as HoverCardPrimitive from "@radix-ui/react-hover-card";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\input-otp.tsx
```text
import * as React from "react";
import { OTPInput, OTPInputContext } from "input-otp";
import { Dot } from "lucide-react";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\input.tsx
```text
import * as React from "react";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\label.tsx
```text
import * as React from "react";
import * as LabelPrimitive from "@radix-ui/react-label";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\menubar.tsx
```text
import * as React from "react";
import * as MenubarPrimitive from "@radix-ui/react-menubar";
import { Check, ChevronRight, Circle } from "lucide-react";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\navigation-menu.tsx
```text
import * as React from "react";
import * as NavigationMenuPrimitive from "@radix-ui/react-navigation-menu";
import { cva } from "class-variance-authority";
import { ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\pagination.tsx
```text
import * as React from "react";
import { ChevronLeft, ChevronRight, MoreHorizontal } from "lucide-react";
import { cn } from "@/lib/utils";
import { ButtonProps, buttonVariants } from "@/components/ui/button";
```

### frontend\bildofy-lms-lovable\src\components\ui\popover.tsx
```text
import * as React from "react";
import * as PopoverPrimitive from "@radix-ui/react-popover";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\progress.tsx
```text
import * as React from "react";
import * as ProgressPrimitive from "@radix-ui/react-progress";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\radio-group.tsx
```text
import * as React from "react";
import * as RadioGroupPrimitive from "@radix-ui/react-radio-group";
import { Circle } from "lucide-react";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\resizable.tsx
```text
import { GripVertical } from "lucide-react";
import * as ResizablePrimitive from "react-resizable-panels";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\scroll-area.tsx
```text
import * as React from "react";
import * as ScrollAreaPrimitive from "@radix-ui/react-scroll-area";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\select.tsx
```text
import * as React from "react";
import * as SelectPrimitive from "@radix-ui/react-select";
import { Check, ChevronDown, ChevronUp } from "lucide-react";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\separator.tsx
```text
import * as React from "react";
import * as SeparatorPrimitive from "@radix-ui/react-separator";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\sheet.tsx
```text
import * as SheetPrimitive from "@radix-ui/react-dialog";
import { cva, type VariantProps } from "class-variance-authority";
import { X } from "lucide-react";
import * as React from "react";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\sidebar.tsx
```text
import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { VariantProps, cva } from "class-variance-authority";
import { PanelLeft } from "lucide-react";
import { useIsMobile } from "@/hooks/use-mobile";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import { Sheet, SheetContent } from "@/components/ui/sheet";
import { Skeleton } from "@/components/ui/skeleton";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
```

### frontend\bildofy-lms-lovable\src\components\ui\skeleton.tsx
```text
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\slider.tsx
```text
import * as React from "react";
import * as SliderPrimitive from "@radix-ui/react-slider";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\sonner.tsx
```text
import { useTheme } from "next-themes";
import { Toaster as Sonner, toast } from "sonner";
```

### frontend\bildofy-lms-lovable\src\components\ui\switch.tsx
```text
import * as React from "react";
import * as SwitchPrimitives from "@radix-ui/react-switch";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\table.tsx
```text
import * as React from "react";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\tabs.tsx
```text
import * as React from "react";
import * as TabsPrimitive from "@radix-ui/react-tabs";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\textarea.tsx
```text
import * as React from "react";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\toast.tsx
```text
import * as React from "react";
import * as ToastPrimitives from "@radix-ui/react-toast";
import { cva, type VariantProps } from "class-variance-authority";
import { X } from "lucide-react";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\toaster.tsx
```text
import { useToast } from "@/hooks/use-toast";
import { Toast, ToastClose, ToastDescription, ToastProvider, ToastTitle, ToastViewport } from "@/components/ui/toast";
```

### frontend\bildofy-lms-lovable\src\components\ui\toggle-group.tsx
```text
import * as React from "react";
import * as ToggleGroupPrimitive from "@radix-ui/react-toggle-group";
import { type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";
import { toggleVariants } from "@/components/ui/toggle";
```

### frontend\bildofy-lms-lovable\src\components\ui\toggle.tsx
```text
import * as React from "react";
import * as TogglePrimitive from "@radix-ui/react-toggle";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\tooltip.tsx
```text
import * as React from "react";
import * as TooltipPrimitive from "@radix-ui/react-tooltip";
import { cn } from "@/lib/utils";
```

### frontend\bildofy-lms-lovable\src\components\ui\use-toast.ts
```text
import { useToast, toast } from "@/hooks/use-toast";
```

### frontend\bildofy-lms-lovable\src\contexts\AuthContext.tsx
```text
import React, { createContext, useContext, useState, useEffect } from "react";
```

### frontend\bildofy-lms-lovable\src\contexts\OnlineContext.tsx
```text
import React, { createContext, useContext, useEffect, useState } from 'react';
```

### frontend\bildofy-lms-lovable\src\hooks\use-mobile.tsx
```text
import * as React from "react";
```

### frontend\bildofy-lms-lovable\src\hooks\use-toast.ts
```text
import * as React from "react";
import type { ToastActionElement, ToastProps } from "@/components/ui/toast";
```

### frontend\bildofy-lms-lovable\src\lib\utils.ts
```text
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
```

### frontend\bildofy-lms-lovable\src\pages\Index.tsx
```text
import { Navigate } from "react-router-dom";
```

### frontend\bildofy-lms-lovable\src\pages\NotFound.tsx
```text
import { useLocation } from "react-router-dom";
import { useEffect } from "react";
```

### frontend\bildofy-lms-lovable\src\pages\RoleSelection.tsx
```text
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { RoleCard } from '@/components/cards/RoleCard';
import { GraduationCap, Users, UserCheck, Sparkles } from 'lucide-react';
```

### frontend\bildofy-lms-lovable\src\pages\auth\LoginPage.tsx
```text
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
```

### frontend\bildofy-lms-lovable\src\pages\auth\SignupPage.tsx
```text
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Link, useNavigate } from "react-router-dom";
```

### frontend\bildofy-lms-lovable\src\pages\parent\ParentDashboard.tsx
```text
import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { StatCard } from '@/components/cards/StatCard';
import { ProgressRing } from '@/components/progress/ProgressRing';
import { XPBar } from '@/components/gamification/XPBar';
import {
```

### frontend\bildofy-lms-lovable\src\pages\student\AssignmentsPage.tsx
```text
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { XPBadge } from '@/components/gamification/XPBadge';
import {
import { cn } from '@/lib/utils';
import { format, isPast, isToday, isTomorrow } from 'date-fns';
```

### frontend\bildofy-lms-lovable\src\pages\student\DoubtChatPage.tsx
```text
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { XPBadge } from '@/components/gamification/XPBadge';
import { useOnlineStatus } from '@/contexts/OnlineContext';
import { ArrowLeft, MessageCircleQuestion, Send, Bot, User, WifiOff, Sparkles } from 'lucide-react';
import { cn } from '@/lib/utils';
```

### frontend\bildofy-lms-lovable\src\pages\student\FlashcardsPage.tsx
```text
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { XPBadge } from '@/components/gamification/XPBadge';
import { ProgressRing } from '@/components/progress/ProgressRing';
import {
import { cn } from '@/lib/utils';
```

### frontend\bildofy-lms-lovable\src\pages\student\NotesPage.tsx
```text
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { XPBadge } from "@/components/gamification/XPBadge";
import { useOnlineStatus } from "@/contexts/OnlineContext";
import {
import { cn } from "@/lib/utils";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";
```

### frontend\bildofy-lms-lovable\src\pages\student\StudentDashboard.tsx
```text
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { StudentHeader } from '@/components/layout/StudentHeader';
import { ActionCard } from '@/components/cards/ActionCard';
import { StatCard } from '@/components/cards/StatCard';
import { AcademicTimeline } from '@/components/timeline/AcademicTimeline';
import { ProgressRing } from '@/components/progress/ProgressRing';
import { XPBadge } from '@/components/gamification/XPBadge';
import {
import { addDays } from 'date-fns';
```

### frontend\bildofy-lms-lovable\src\pages\student\TestsPage.tsx
```text
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { XPBadge } from '@/components/gamification/XPBadge';
import { ProgressRing } from '@/components/progress/ProgressRing';
import { useOnlineStatus } from '@/contexts/OnlineContext';
import {
import { cn } from '@/lib/utils';
```

### frontend\bildofy-lms-lovable\src\pages\student\WatchVideosPage.tsx
```text
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { ArrowLeft, Video } from 'lucide-react';
```

### frontend\bildofy-lms-lovable\src\pages\teacher\AIContentPage.tsx
```text
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { ArrowLeft, Sparkles } from 'lucide-react';
```

### frontend\bildofy-lms-lovable\src\pages\teacher\AnalyticsPage.tsx
```text
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { ArrowLeft, BarChart3 } from 'lucide-react';
```

### frontend\bildofy-lms-lovable\src\pages\teacher\CreateAssignmentPage.tsx
```text
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ArrowLeft, FileText } from 'lucide-react';
```

### frontend\bildofy-lms-lovable\src\pages\teacher\CreateTestPage.tsx
```text
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ArrowLeft, ClipboardCheck } from 'lucide-react';
```

### frontend\bildofy-lms-lovable\src\pages\teacher\SubmissionsPage.tsx
```text
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';
```

### frontend\bildofy-lms-lovable\src\pages\teacher\TeacherDashboard.tsx
```text
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { StatCard } from '@/components/cards/StatCard';
import {
```

