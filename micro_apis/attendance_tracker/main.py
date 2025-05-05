import uvicorn
import csv
from datetime import date
from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io

from database import get_db, engine
import models
import schemas
from utils.attendance_cache import get_today_str

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Attendance Tracker")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Team Member endpoints
@app.post("/api/team-members/", response_model=schemas.TeamMember)
def create_team_member(team_member: schemas.TeamMemberCreate, db: Session = Depends(get_db)):
    db_member = db.query(models.TeamMember).filter(models.TeamMember.email_id == team_member.email_id).first()
    if db_member:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_member = models.TeamMember(**team_member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

@app.get("/api/team-members/", response_model=List[schemas.TeamMember])
def read_team_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    team_members = db.query(models.TeamMember).offset(skip).limit(limit).all()
    return team_members

# Attendance endpoints
@app.post("/api/attendance/", response_model=schemas.AttendanceRecord)
def create_attendance_record(attendance: schemas.AttendanceRecordCreate, db: Session = Depends(get_db)):
    # Find team member by email
    team_member = db.query(models.TeamMember).filter(models.TeamMember.email_id == attendance.team_member_email_id).first()
    if not team_member:
        raise HTTPException(status_code=404, detail="Team member not found")
    
    # Check if attendance for this date already exists
    existing_record = db.query(models.AttendanceRecord).filter(
        models.AttendanceRecord.date == attendance.date,
        models.AttendanceRecord.team_member_id == team_member.id
    ).first()
    
    if existing_record:
        # Update existing record
        for key, value in attendance.dict().items():
            if key not in ["team_member_email_id"]:
                setattr(existing_record, key, value)
        db.commit()
        db.refresh(existing_record)
        
        result = schemas.AttendanceRecord(
            id=existing_record.id,
            date=existing_record.date,
            team_member_email_id=team_member.email_id,
            team_member_name=team_member.name,
            first_quarter=existing_record.first_quarter,
            second_quarter=existing_record.second_quarter,
            third_quarter=existing_record.third_quarter,
            fourth_quarter=existing_record.fourth_quarter
        )
        return result
    
    # Create new record
    db_attendance = models.AttendanceRecord(
        date=attendance.date,
        team_member_id=team_member.id,
        first_quarter=attendance.first_quarter,
        second_quarter=attendance.second_quarter,
        third_quarter=attendance.third_quarter,
        fourth_quarter=attendance.fourth_quarter
    )
    
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    
    # Return with team member information
    result = schemas.AttendanceRecord(
        id=db_attendance.id,
        date=db_attendance.date,
        team_member_email_id=team_member.email_id,
        team_member_name=team_member.name,
        first_quarter=db_attendance.first_quarter,
        second_quarter=db_attendance.second_quarter,
        third_quarter=db_attendance.third_quarter,
        fourth_quarter=db_attendance.fourth_quarter
    )
    return result

@app.get("/api/attendance/", response_model=List[schemas.AttendanceRecord])
def read_attendance_records(date_filter: Optional[date] = Query(None), db: Session = Depends(get_db)):
    query = db.query(
        models.AttendanceRecord,
        models.TeamMember.name,
        models.TeamMember.email_id
    ).join(models.TeamMember)
    
    if date_filter:
        query = query.filter(models.AttendanceRecord.date == date_filter)
    
    records = query.all()
    
    result = []
    for record, name, email in records:
        result.append(schemas.AttendanceRecord(
            id=record.id,
            date=record.date,
            team_member_email_id=email,
            team_member_name=name,
            first_quarter=record.first_quarter,
            second_quarter=record.second_quarter,
            third_quarter=record.third_quarter,
            fourth_quarter=record.fourth_quarter
        ))
    
    return result

@app.get("/api/attendance/export/")
def export_attendance_csv(date_filter: date, db: Session = Depends(get_db)):
    query = db.query(
        models.AttendanceRecord,
        models.TeamMember
    ).join(models.TeamMember).filter(models.AttendanceRecord.date == date_filter)
    
    records = query.all()
    
    # Create in-memory CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        "Date", "Name", "Email", "First Quarter", "Second Quarter", 
        "Third Quarter", "Fourth Quarter"
    ])
    
    # Write data
    for record, member in records:
        writer.writerow([
            record.date,
            member.name,
            member.email_id,
            "Present" if record.first_quarter else "Absent",
            "Present" if record.second_quarter else "Absent",
            "Present" if record.third_quarter else "Absent",
            "Present" if record.fourth_quarter else "Absent"
        ])
    
    output.seek(0)
    
    # Return CSV file for download
    return StreamingResponse(
        iter([output.getvalue()]), 
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment;filename=attendance_{date_filter}.csv"}
    )

@app.get("/")
def read_root():
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80, log_level="info")