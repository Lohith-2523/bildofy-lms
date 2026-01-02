from fastapi import Depends
from app.security import require_role
from app.security.roles import Role

admin_guard = Depends(require_role(Role.ADMIN))
