from fastapi import APIRouter

router = APIRouter(prefix="/risk-zones", tags=["risk-zones"])


@router.get("")
async def list_risk_zones():
    """Return all risk zones with current risk level (GeoJSON)."""
    return {"type": "FeatureCollection", "features": []}


@router.get("/{zone_id}/history")
async def get_risk_zone_history(zone_id: int):
    """Return risk trend over time for one zone."""
    return {"zone_id": zone_id, "history": []}


@router.get("/{zone_id}/explanation")
async def get_risk_zone_explanation(zone_id: int):
    """Return human-readable explanation of why a zone is at its current risk level."""
    return {
        "zone_id": zone_id,
        "risk_level": "Low",
        "explanation": "Threshold not exceeded. No ML flags active.",
        "thresholds_checked": [],
        "actual_readings": [],
    }
