from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import RiskZone
from app.db.session import get_session

router = APIRouter(prefix="/risk-zones", tags=["risk-zones"])


@router.get("")
async def list_risk_zones(session: AsyncSession = Depends(get_session)):
    """Return all risk zones with current risk level (GeoJSON)."""
    result = await session.execute(
        text(
            """
            SELECT
                id,
                zone_name,
                district,
                state,
                current_risk_level,
                last_computed_at,
                ST_AsGeoJSON(geom)::json AS geometry
            FROM risk_zones
            """
        )
    )
    rows = result.mappings().all()

    features = []
    for row in rows:
        features.append(
            {
                "type": "Feature",
                "geometry": row["geometry"],
                "properties": {
                    "id": row["id"],
                    "zone_name": row["zone_name"],
                    "district": row["district"],
                    "state": row["state"],
                    "current_risk_level": row["current_risk_level"],
                    "last_computed_at": row["last_computed_at"],
                },
            }
        )

    return {"type": "FeatureCollection", "features": features}


@router.get("/{zone_id}/history")
async def get_risk_zone_history(zone_id: int):
    """Return risk trend over time for one zone."""
    return {"zone_id": zone_id, "history": []}


@router.get("/{zone_id}/explanation")
async def get_risk_zone_explanation(zone_id: int, session: AsyncSession = Depends(get_session)):
    """Return human-readable explanation of why a zone is at its current risk level."""
    result = await session.execute(
        text(
            """
            SELECT id, zone_name, current_risk_level
            FROM risk_zones
            WHERE id = :zone_id
            """
        ),
        {"zone_id": zone_id},
    )
    row = result.mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="Zone not found")

    zone_name = row["zone_name"]
    risk_level = row["current_risk_level"]

    # NE Himalaya moisture threshold: E(mm) = -11.10 + 0.62 * D(hr)
    # For 72 hours: E = -11.10 + 0.62 * 72 = 33.54 mm (base)
    # But published regional thresholds are higher due to local conditions
    explanations = {
        "Low": {
            "explanation": "72-hr cumulative rainfall of 28mm is below this zone's regional threshold of 120mm (NE Himalaya moisture threshold).",
            "thresholds": [
                {"name": "NE Himalaya moisture threshold (72hr)", "threshold_value": 120, "actual_value": 28},
            ],
        },
        "Moderate": {
            "explanation": "72-hr cumulative rainfall of 142mm exceeds this zone's regional threshold of 120mm but remains below the high-risk threshold of 180mm (NE Himalaya moisture threshold).",
            "thresholds": [
                {"name": "NE Himalaya moisture threshold (72hr)", "threshold_value": 120, "actual_value": 142},
            ],
        },
        "High": {
            "explanation": "72-hr cumulative rainfall of 205mm exceeds this zone's high-risk threshold of 180mm (NE Himalaya moisture threshold) and approaches severe levels.",
            "thresholds": [
                {"name": "NE Himalaya moisture threshold (72hr) - high", "threshold_value": 180, "actual_value": 205},
            ],
        },
        "Severe": {
            "explanation": "72-hr cumulative rainfall of 245mm exceeds this zone's regional threshold of 180mm (NE Himalaya moisture threshold) by a wide margin.",
            "thresholds": [
                {"name": "NE Himalaya moisture threshold (72hr) - severe", "threshold_value": 180, "actual_value": 245},
            ],
        },
    }

    exp = explanations.get(risk_level, explanations["Low"])

    return {
        "zone_id": zone_id,
        "zone_name": zone_name,
        "risk_level": risk_level,
        "explanation": exp["explanation"],
        "thresholds_checked": exp["thresholds"],
        "mock_data": True,
    }
