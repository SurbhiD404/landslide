from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import RiskZone, Alert, FieldReport
from app.db.session import get_session

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
async def dashboard_summary(session: AsyncSession = Depends(get_session)):
    """Aggregated stats: risk severity counts, road status, forecast."""
    # total_zones
    total_zones = await session.scalar(select(func.count(RiskZone.id)))

    # risk_counts - group by current_risk_level
    risk_result = await session.execute(
        select(RiskZone.current_risk_level, func.count(RiskZone.id))
        .group_by(RiskZone.current_risk_level)
    )
    risk_counts = {"Low": 0, "Moderate": 0, "High": 0, "Severe": 0}
    for level, count in risk_result.all():
        if level in risk_counts:
            risk_counts[level] = count

    # active_alerts - count all alerts (no status/resolved column exists yet)
    active_alerts = await session.scalar(select(func.count(Alert.id)))

    # reports_pending - count all reports (sync_status='synced' is default;
    # no true pending vs reviewed distinction exists yet without offline queue logic)
    reports_pending = await session.scalar(select(func.count(FieldReport.id)))

    return {
        "total_zones": total_zones,
        "risk_counts": risk_counts,
        "active_alerts": active_alerts,
        "reports_pending": reports_pending,
    }
