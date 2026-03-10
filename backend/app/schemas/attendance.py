from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class AttendanceMarkItem(BaseModel):
    student_id: int
    present: bool
    remark: Optional[str] = None


class AttendanceMarkRequest(BaseModel):
    subject_id: int
    attendance_date: date
    records: List[AttendanceMarkItem]


class AttendanceStudentRow(BaseModel):
    student_id: int
    name: str
    present: Optional[bool] = None
    remark: Optional[str] = None


class StudentAttendanceRecordResponse(BaseModel):
    attendance_date: date
    subject_id: int
    subject_name: str
    present: bool
    remark: Optional[str] = None
