from pydantic import BaseModel, Field
from typing import List, Optional, Dict

# --- Profile Schemas ---

class PersonalInfo(BaseModel):
    name: str = Field(..., description="Full Name")
    email: Optional[str] = ""
    phone: Optional[str] = ""
    linkedin: Optional[str] = ""
    location: Optional[str] = ""

class Experience(BaseModel):
    company: str
    title: str
    dates: Optional[str] = ""
    location: Optional[str] = ""
    responsibilities: List[str] = Field(default_factory=list)

class Education(BaseModel):
    school: str
    degree: str
    field: Optional[str] = ""
    dates: Optional[str] = ""

class Profile(BaseModel):
    personal_info: PersonalInfo
    summary: str = ""
    skills: Dict[str, List[str]] = Field(default_factory=dict)
    experience: List[Experience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)


# --- Job Analysis Schemas ---

class RoleInfo(BaseModel):
    title: str
    company: Optional[str] = "Unknown"
    location: Optional[str] = "Unknown"
    level: Optional[str] = "Mid"

class Requirements(BaseModel):
    must_have_skills: List[str] = Field(default_factory=list)
    nice_to_have_skills: List[str] = Field(default_factory=list)
    education: Optional[str] = ""
    years_experience: Optional[str] = ""

class Keywords(BaseModel):
    ats_keywords: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)

class JobAnalysis(BaseModel):
    role_info: RoleInfo
    requirements: Requirements
    keywords: Keywords
    summary: str = ""
