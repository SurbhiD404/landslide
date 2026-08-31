from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
async def dashboard_summary():
    """Aggregated stats: risk severity counts, road status, forecast."""
    return {
        "total_zones": 0,
        "risk_counts": {"Low": 0, "Moderate": 0, "High": 0, "Severe": 0},
        "active_alerts": 0,
        "reports_pending": 0,
    }
