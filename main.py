from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone
import logging

from scoring import calculate_accessibility_score

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AccessBuild API",
    description="AI-powered accessibility audit tool for mobile apps",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODELS
# ============================================================
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


# ============================================================
# ENDPOINTS
# ============================================================
@app.get("/")
async def health_check():
    return {
        "status": "alive",
        "service": "AccessBuild API",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.post("/audit", response_model=AuditResponse)
async def audit_app(request: AuditRequest):
    """
    Accepts a list of UI elements and returns an accessibility score.
    """
    try:
        logger.info(f"Auditing {request.app_name} - {len(request.elements)} elements")

        result = calculate_accessibility_score(request.elements)

        return AuditResponse(
            app_name=request.app_name,
            package_name=request.package_name,
            screen_name=request.screen_name or "Main Screen",
            score=result["score"],
            grade=result["grade"],
            total_elements=result["total"],
            labeled_elements=result["labeled"],
            unlabeled_elements=result["unlabeled"],
            accessibility_percentage=result["percentage"],
            recommendation=result["recommendation"],
            timestamp=datetime.now(timezone.utc)
        )

    except Exception as e:
        logger.error(f"Audit error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/grades")
async def get_grading_system():
    """Returns the accessibility grading system explanation."""
    return {
        "A": "90%+ elements labeled. Fully accessible to screen readers.",
        "B": "70-89% labeled. Mostly accessible. Minor gaps.",
        "C": "50-69% labeled. Partially accessible. Needs work.",
        "D": "25-49% labeled. Mostly inaccessible. Urgent fixes needed.",
        "F": "Below 25% labeled. Completely inaccessible to blind users."
    }