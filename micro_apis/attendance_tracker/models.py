from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    status = Column(String, default="active")
    
    attendance_records = relationship("AttendanceRecord", back_populates="team_member")

class AttendanceRecord(Base):
    __tablename__ = "attendance_records"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    team_member_id = Column(Integer, ForeignKey("team_members.id"))
    first_quarter = Column(Boolean, default=True)
    second_quarter = Column(Boolean, default=True)
    third_quarter = Column(Boolean, default=True)
    fourth_quarter = Column(Boolean, default=True)
    
    team_member = relationship("TeamMember", back_populates="attendance_records")
