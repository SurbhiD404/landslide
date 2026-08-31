from fastapi import APIRouter

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("")
async def list_alerts(district: str | None = None, since: str | None = None):
    """Return alert history, optionally filtered by district and since timestamp."""
    return {"alerts": []}


@router.post("/dispatch")
async def dispatch_alert():
    """Manually trigger an alert (admin override)."""
    return {"status": "dispatched", "alert_id": None}
