from app.services.notes_service import generate_notes
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
    create_ai_assisted_notes,
    upload_notes_file,
)
from app.services.file_validation import validate_upload
