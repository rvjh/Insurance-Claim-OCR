from fastapi import APIRouter
from sqlalchemy import text
from db.database import SessionLocal

router = APIRouter()


@router.get("/admin/metrics")
def admin_metrics():

    db = SessionLocal()

    total_users = db.execute(
        text("SELECT COUNT(DISTINCT user_id) FROM claim_logs")
    ).scalar()

    total_claims = db.execute(
        text("SELECT COUNT(*) FROM claim_logs")
    ).scalar()

    approved = db.execute(
        text("SELECT COUNT(*) FROM claim_logs WHERE status = 'True'")
    ).scalar()

    rejected = db.execute(
        text("SELECT COUNT(*) FROM claim_logs WHERE status = 'False'")
    ).scalar()

    car_detected = db.execute(
        text("SELECT COUNT(*) FROM claim_logs WHERE car_detected = 1")
    ).scalar()

    return {
        "total_users": total_users,
        "total_claims": total_claims,
        "approved_claims": approved,
        "rejected_claims": rejected,
        "car_detected_cases": car_detected
    }