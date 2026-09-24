import os
import logging
from supabase import create_client, Client

logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    logger.warning("Supabase credentials not set.")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def save_audit(app_name, package_name, screen_name, result, raw_xml=None):
    if not supabase:
        logger.warning("Supabase not configured. Skipping save.")
        return None

    try:
        record = {
            "app_name": app_name,
            "package_name": package_name,
            "screen_name": screen_name,
            "score": result["score"],
            "grade": result["grade"],
            "total_elements": result["total"],
            "labeled_elements": result["labeled"],
            "unlabeled_elements": result["unlabeled"],
            "accessibility_percentage": result["percentage"],
            "recommendation": result["recommendation"],
            "raw_xml": raw_xml
        }
        response = supabase.table("audits").insert(record).execute()
        logger.info(f"Audit saved: {app_name} - {result['score']}")
        return response.data
    except Exception as e:
        logger.error(f"Supabase save error: {e}")
        return None


def get_recent_audits(limit: int = 20) -> list:
    if not supabase:
        return []
    try:
        response = (
            supabase.table("audits")
            .select("*")
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data
    except Exception as e:
        logger.error(f"Supabase fetch error: {e}")
        return []


def get_audit_stats() -> dict:
    if not supabase:
        return {"error": "Supabase not configured"}
    try:
        response = supabase.table("audits").select("*").execute()
        audits = response.data

        if not audits:
            return {"total_audits": 0, "average_accessibility": 0, "grade_distribution": {}}

        total = len(audits)
        avg = sum(a["accessibility_percentage"] for a in audits) / total

        grade_counts = {}
        for a in audits:
            grade = a["score"]
            grade_counts[grade] = grade_counts.get(grade, 0) + 1

        return {
            "total_audits": total,
            "average_accessibility": round(avg, 1),
            "grade_distribution": grade_counts
        }
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return {"error": str(e)}