"""IMD rainfall data ingestion client.

This is a stub. IMD does not provide a public REST API. Integration
requires institutional MoU or manual FTP download.

TODO: Replace with real IMD API endpoint when credentials are obtained.
Format reference: IMD's known CSV format (station_id, timestamp, rainfall_mm).
"""


async def fetch_rainfall(station_id: str) -> list[dict]:
    """Fetch rainfall data for a station.

    Returns:
        List of dicts with keys: station_id, timestamp, rainfall_mm.
    """
    return []
