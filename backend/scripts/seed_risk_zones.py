import asyncio
import sys
from pathlib import Path
from datetime import datetime
from sqlalchemy import text

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.session import async_session

ZONES = [
    {
        "zone_name": "Guwahati North",
        "district": "Kamrup Metropolitan",
        "state": "Assam",
        "current_risk_level": "Low",
        "geom": "POLYGON((91.70 26.20, 91.71 26.20, 91.71 26.21, 91.70 26.21, 91.70 26.20))",
    },
    {
        "zone_name": "Guwahati South",
        "district": "Kamrup Metropolitan",
        "state": "Assam",
        "current_risk_level": "Low",
        "geom": "POLYGON((91.71 26.19, 91.72 26.19, 91.72 26.20, 91.71 26.20, 91.71 26.19))",
    },
    {
        "zone_name": "Dispur",
        "district": "Kamrup Metropolitan",
        "state": "Assam",
        "current_risk_level": "Moderate",
        "geom": "POLYGON((91.72 26.18, 91.73 26.18, 91.73 26.19, 91.72 26.19, 91.72 26.18))",
    },
    {
        "zone_name": "Chandrapur",
        "district": "Kamrup Metropolitan",
        "state": "Assam",
        "current_risk_level": "High",
        "geom": "POLYGON((91.73 26.17, 91.74 26.17, 91.74 26.18, 91.73 26.18, 91.73 26.17))",
    },
    {
        "zone_name": "Sonapur",
        "district": "Kamrup Metropolitan",
        "state": "Assam",
        "current_risk_level": "Severe",
        "geom": "POLYGON((91.74 26.16, 91.75 26.16, 91.75 26.17, 91.74 26.17, 91.74 26.16))",
    },
]


async def seed():
    async with async_session() as session:
        for z in ZONES:
            await session.execute(
                text(
                    """
                    INSERT INTO risk_zones (zone_name, district, state, current_risk_level, geom, last_computed_at)
                    VALUES (:zone_name, :district, :state, :current_risk_level,
                            ST_SetSRID(ST_GeomFromText(:geom), 4326), :last_computed_at)
                    """
                ),
                {
                    "zone_name": z["zone_name"],
                    "district": z["district"],
                    "state": z["state"],
                    "current_risk_level": z["current_risk_level"],
                    "geom": z["geom"],
                    "last_computed_at": datetime.utcnow(),
                },
            )
        await session.commit()
        print(f"Inserted {len(ZONES)} risk zones")


if __name__ == "__main__":
    asyncio.run(seed())