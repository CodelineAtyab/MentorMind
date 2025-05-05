from datetime import date
from typing import List, Optional
from pydantic import BaseModel, EmailStr

# Team Member Schemas
class TeamMemberBase(BaseModel):
    email_id: EmailStr
    name: str
    status: Optional[str] = "active"

class TeamMemberCreate(TeamMemberBase):
    pass

class TeamMember(TeamMemberBase):
    id: int

    class Config:
        orm_mode = True

# Attendance Record Schemas
class AttendanceRecordBase(BaseModel):
    date: date
    team_member_email_id: EmailStr
    first_quarter: Optional[bool] = True
    second_quarter: Optional[bool] = True
    third_quarter: Optional[bool] = True
    fourth_quarter: Optional[bool] = True

class AttendanceRecordCreate(AttendanceRecordBase):
    pass

class AttendanceRecord(AttendanceRecordBase):
    id: int
    team_member_name: str

    class Config:
        orm_mode = True

class AttendanceFilter(BaseModel):
    date: date
