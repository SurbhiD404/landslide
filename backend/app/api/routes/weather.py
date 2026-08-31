from fastapi import APIRouter

router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/forecast")
async def get_weather_forecast(zone_id: int | None = None):
    """IMD-linked forecast for a zone."""
    return {"zone_id": zone_id, "forecast": []}
