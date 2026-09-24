from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Element(BaseModel):
    id: str
    type: str = Field(..., description="button, input, icon, link, etc.")
    label: Optional[str] = Field(default=None, description="Accessibility label (content-desc)")
    text: Optional[str] = Field(default=None, description="Visible text on element")


class AuditRequest(BaseModel):
    app_name: str
    package_name: Optional[str] = None
    elements: List[Element]
    screen_name: Optional[str] = "Main Screen"


class AuditResponse(BaseModel):
    app_name: str
    package_name: Optional[str]
    screen_name: str
    score: str
    grade: str
    total_elements: int
    labeled_elements: int
    unlabeled_elements: int
    accessibility_percentage: float
    recommendation: str
    timestamp: datetime


class ScanRequest(BaseModel):
    app_name: str
    package_name: Optional[str] = None
    screen_name: Optional[str] = "Main Screen"
    ui_tree_xml: str = Field(..., description="Raw Android UI tree XML dump")


class ScanResponse(BaseModel):
    app_name: str
    package_name: Optional[str]
    screen_name: str
    score: str
    grade: str
    total_elements: int
    labeled_elements: int
    unlabeled_elements: int
    accessibility_percentage: float
    recommendation: str
    timestamp: datetime