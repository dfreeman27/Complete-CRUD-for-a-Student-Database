from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Optional

from app.schemas.student import StudentCreate, StudentUpdate, StudentPatch, StudentResponse
from app.models.student import Student
from app.database import get_db

router = APIRouter(prefix="/students", tags=["Students"])


def get_student_or_404(student_id: int, db: Session) -> Student:
    """Fetches a student by ID or raises a 404 if not found."""
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """
    Creates a new student.
    """
    db_student = Student(**student.model_dump())
    try:
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Student already exists..")
    return db_student


@router.get("/", response_model=list[StudentResponse])
def list_students(
    major: Optional[str] = Query(None),
    min_gpa: Optional[float] = Query(None, ge=0.0, le=4.0),
    db: Session = Depends(get_db),
):
    """
    Returns students, optionally filtered by major and/or minimum GPA.
    """
    query = db.query(Student)
    if major:
        query = query.filter(Student.major == major)
    if min_gpa is not None:
        query = query.filter(Student.gpa >= min_gpa)
    return query.all()


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """Returns a single student by ID."""
    return get_student_or_404(student_id, db)


@router.put("/{student_id}", response_model=StudentResponse)
def replace_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    """
    Fully replaces a student record (all fields required).
    """
    db_student = get_student_or_404(student_id, db)

    for field, value in student.model_dump().items():
        setattr(db_student, field, value)

    try:
        db.commit()
        db.refresh(db_student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Student already exists..")

    return db_student


@router.patch("/{student_id}", response_model=StudentResponse)
def patch_student(student_id: int, student: StudentPatch, db: Session = Depends(get_db)):
    """
    Partially updates a student (only fields sent are changed).
    """
    db_student = get_student_or_404(student_id, db)

    update_data = student.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_student, field, value)

    try:
        db.commit()
        db.refresh(db_student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Student already exists..")

    return db_student


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """
    Deletes a student by ID.
    """
    db_student = get_student_or_404(student_id, db)

    db.delete(db_student)
    db.commit()

    return {"message": f"Student {student_id} deleted successfully"}