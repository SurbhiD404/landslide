from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.models import FieldReport, User
from app.db.session import get_session

router = APIRouter(prefix="/reports", tags=["reports"])


class SubmitReportRequest(BaseModel):
    latitude: float
    longitude: float
    report_type: str  # crack, slope_movement, road_blocked
    description: str | None = None


@router.post("")
async def submit_report(
    request: SubmitReportRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Submit a citizen/field report (supports offline queue replay)."""
    # Find containing risk zone via spatial query
    zone_result = await session.execute(
        text(
            """
            SELECT id FROM risk_zones
            WHERE ST_Contains(geom, ST_SetSRID(ST_GeomFromText(:point), 4326))
            LIMIT 1
            """
        ),
        {"point": f"POINT({request.longitude} {request.latitude})"},
    )
    zone_id = zone_result.scalar_one_or_none()

    # Insert FieldReport with geom from lat/lng and auto-computed zone_id
    result = await session.execute(
        text(
            """
            INSERT INTO field_reports (user_id, zone_id, geom, photo_url, video_url, description, report_type, submitted_at, sync_status)
            VALUES (:user_id, :zone_id, ST_SetSRID(ST_GeomFromText(:geom), 4326), NULL, NULL, :description, :report_type, NOW(), 'synced')
            RETURNING id
            """
        ),
        {
            "user_id": current_user.id,
            "zone_id": zone_id,
            "geom": f"POINT({request.longitude} {request.latitude})",
            "description": request.description,
            "report_type": request.report_type,
        },
    )
    await session.commit()
    report_id = result.scalar_one()
    return {"status": "accepted", "report_id": report_id, "zone_id": zone_id}


@router.get("")
async def list_reports(
    zone_id: int | None = None,
    report_type: str | None = None,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """List reports, optionally filtered by zone_id and report_type."""
    query = """
        SELECT
            id,
            user_id,
            zone_id,
            report_type,
            description,
            ST_X(geom) AS longitude,
            ST_Y(geom) AS latitude,
            submitted_at,
            sync_status
        FROM field_reports
    """
    params = {}
    conditions = []
    if zone_id is not None:
        conditions.append("zone_id = :zone_id")
        params["zone_id"] = zone_id
    if report_type:
        conditions.append("report_type = :report_type")
        params["report_type"] = report_type
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY submitted_at DESC"
    result = await session.execute(text(query), params)
    rows = result.mappings().all()
    return {"reports": [dict(row) for row in rows]}
