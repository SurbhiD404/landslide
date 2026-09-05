from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.mock_explanations import get_explanation_for_risk_level
from app.db.models import Alert, RiskZone
from app.db.session import get_session

router = APIRouter(prefix="/alerts", tags=["alerts"])


class DispatchAlertRequest(BaseModel):
    zone_id: int


@router.get("")
async def list_alerts(
    district: Optional[str] = None,
    since: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
):
    """Return alert history, optionally filtered by district and since timestamp."""
    query = """
        SELECT
            a.id,
            a.zone_id,
            rz.zone_name,
            a.risk_level,
            a.message,
            a.language,
            a.channel,
            a.dispatched_at,
            a.explanation
        FROM alerts a
        JOIN risk_zones rz ON a.zone_id = rz.id
    """
    params = {}
    conditions = []

    if district:
        conditions.append("rz.district = :district")
        params["district"] = district

    if since:
        conditions.append("a.dispatched_at >= :since")
        params["since"] = since

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY a.dispatched_at DESC"

    result = await session.execute(text(query), params)
    rows = result.mappings().all()
    return {"alerts": [dict(row) for row in rows]}


@router.post("/dispatch")
async def dispatch_alert(
    request: DispatchAlertRequest,
    session: AsyncSession = Depends(get_session),
):
    """Manually trigger an alert (admin override)."""
    from fastapi import HTTPException, status

    # Look up zone
    result = await session.execute(
        select(RiskZone).where(RiskZone.id == request.zone_id)
    )
    zone = result.scalar_one_or_none()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")

    risk_level = zone.current_risk_level
    exp = get_explanation_for_risk_level(risk_level)

    # Create alert row
    alert = Alert(
        zone_id=request.zone_id,
        risk_level=risk_level,
        message=exp["explanation"],
        language="en",
        channel="mock",
        dispatched_at=datetime.utcnow(),
        explanation=exp["explanation"],
    )
    session.add(alert)
    try:
        await session.flush()
        await session.refresh(alert)
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    return {"status": "dispatched", "alert_id": alert.id}
