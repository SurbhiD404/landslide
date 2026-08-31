"""DEM/slope data loader for PostGIS.

This is a stub. Bhuvan (ISRO) requires registration and approval.
DEM data can alternatively be sourced from SRTM or ASTER GDEM.

TODO: Replace with real Bhuvan WMS/WCS or direct GeoTIFF load.
For now, accepts a GeoTIFF path and stores raster metadata.
"""

from pathlib import Path


def load_dem_to_postgis(tiff_path: Path) -> dict:
    """Load a GeoTIFF DEM into PostGIS using raster2pgsql.

    Args:
        tiff_path: Path to the GeoTIFF file.

    Returns:
        dict with status and row count.
    """
    if not tiff_path.exists():
        return {"status": "error", "message": f"File not found: {tiff_path}"}
    return {
        "status": "stub",
        "message": "Raster loading requires raster2pgsql integration",
    }
