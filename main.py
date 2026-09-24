from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import logging

from models import AuditRequest, AuditResponse, ScanRequest, ScanResponse
from scoring import calculate_accessibility_score
from parser import parse_ui_tree
from database import save_audit, get_recent_audits, get_audit_stats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AccessBuild API",
    description="AI-powered accessibility audit tool for mobile apps",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/")
async def health_check():
    return {
        "status": "alive",
        "service": "AccessBuild API",
        "version": "2.0.0",
        "endpoints": {
            "/audit": "POST - Manual audit from element list",
            "/scan": "POST - Auto-scan from Android UI tree XML",
            "/audits/recent": "GET - Recent audits",
            "/stats": "GET - Aggregate statistics"
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.post("/audit", response_model=AuditResponse)
async def audit_app(request: AuditRequest):
    try:
        logger.info(f"Manual audit: {request.app_name} ({len(request.elements)} elements)")
        result = calculate_accessibility_score(request.elements)

        save_audit(
            app_name=request.app_name,
            package_name=request.package_name,
            screen_name=request.screen_name or "Main Screen",
            result=result,
            raw_xml=None
        )

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


@app.post("/scan", response_model=ScanResponse)
async def scan_ui_tree(request: ScanRequest):
    try:
        logger.info(f"Scanning {request.app_name} from UI tree XML")
        elements = parse_ui_tree(request.ui_tree_xml)

        if not elements:
            raise HTTPException(status_code=400, detail="No elements found in XML")

        logger.info(f"Parsed {len(elements)} elements")
        result = calculate_accessibility_score(elements)

        save_audit(
            app_name=request.app_name,
            package_name=request.package_name,
            screen_name=request.screen_name or "Main Screen",
            result=result,
            raw_xml=request.ui_tree_xml
        )

        return ScanResponse(
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

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Scan error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/audits/recent")
async def recent_audits(limit: int = 20):
    try:
        audits = get_recent_audits(limit)
        return {"count": len(audits), "audits": audits}
    except Exception as e:
        logger.error(f"Fetch recent error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def stats():
    try:
        return get_audit_stats()
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/grades")
async def get_grading_system():
    return {
        "A": "90%+ elements labeled. Fully accessible to screen readers.",
        "B": "70-89% labeled. Mostly accessible. Minor gaps.",
        "C": "50-69% labeled. Partially accessible. Needs work.",
        "D": "25-49% labeled. Mostly inaccessible. Urgent fixes needed.",
        "F": "Below 25% labeled. Completely inaccessible to blind users."
    }
