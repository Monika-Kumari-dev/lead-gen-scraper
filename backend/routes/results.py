"""
GET /api/results - fetch stored leads for the dashboard's results table.
Supports basic filtering, which the frontend "Search form" will map to.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from models.lead import Lead

router = APIRouter()


@router.get("/")
def get_results(
    region: Optional[str] = None,
    industry: Optional[str] = None,
    qa_status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Lead)

    if region:
        query = query.filter(Lead.region == region)
    if industry:
        query = query.filter(Lead.industry == industry)
    if qa_status:
        query = query.filter(Lead.qa_status == qa_status)

    return query.all()


@router.patch("/{lead_id}/qa")
def update_qa(lead_id: int, qa_status: str, fail_reason: Optional[str] = None, db: Session = Depends(get_db)):
    """Used by the manual spot-check step to log pass/fail + reason."""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        return {"error": "Lead not found"}

    lead.qa_status = qa_status
    lead.fail_reason = fail_reason
    db.commit()
    return {"updated": lead_id, "qa_status": qa_status, "fail_reason": fail_reason}
