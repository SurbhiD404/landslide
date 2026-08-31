from fastapi import APIRouter

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("")
async def submit_report():
    """Submit a citizen/field report (supports offline queue replay)."""
    return {"status": "accepted", "report_id": None}


@router.get("")
async def list_reports(zone_id: int | None = None, status: str | None = None):
    """List reports, optionally filtered by zone_id and status."""
    return {"reports": []}
