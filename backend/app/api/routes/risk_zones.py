from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.mock_explanations import get_explanation_for_risk_level
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

    exp = get_explanation_for_risk_level(risk_level)

    return {
        "zone_id": zone_id,
        "zone_name": zone_name,
        "risk_level": risk_level,
        "explanation": exp["explanation"],
        "thresholds_checked": exp["thresholds"],
        "mock_data": True,
    }
