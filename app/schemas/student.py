
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional


class StudentCreate(BaseModel):
    """Schema for creating a student."""
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(max_length=200)
    major: Optional[str] = None
    gpa: Optional[float] = Field(default=None, ge=0, le=4)

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("email must contain '@'")
        return v


class StudentUpdate(BaseModel):
    """Schema for fully replacing a student (PUT)."""
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(max_length=200)
    major: Optional[str] = None
    gpa: Optional[float] = Field(default=None, ge=0, le=4)



class StudentPatch(BaseModel):
    """Schema for partially updating a student (PATCH)."""
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[str] = Field(default=None, max_length=200)
    major: Optional[str] = None
    gpa: Optional[float] = Field(default=None, ge=0, le=4)



class StudentResponse(BaseModel):
    """Schema for returning student data."""
    id: int
    name: str
    email: str
    major: Optional[str]
    gpa: Optional[float]


    model_config = ConfigDict(from_attributes=True)