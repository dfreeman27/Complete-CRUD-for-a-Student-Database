
from sqlalchemy import CheckConstraint, String, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Student(Base):
    """SQLAlchemy model for the students table."""
    __tablename__ = "students"
    __table_args__ = (
        CheckConstraint("gpa >= 0.0 AND gpa <= 4.0", name="ck_students_gpa_range"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    major: Mapped[str] = mapped_column(String(100), nullable=True)
    gpa: Mapped[float] = mapped_column(Float, nullable=True,)