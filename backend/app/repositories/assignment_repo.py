from ..models.assignments import Assignment
from .base_repo import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession


class AssignmentRepo(BaseRepo[Assignment]):
    def __init__(self):
        super().__init__(Assignment)
