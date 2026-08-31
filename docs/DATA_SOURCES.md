# Data Sources

## IMD Rainfall Data

- **Source:** India Meteorological Department
- **Access:** No public REST API. Requires institutional MoU or manual FTP download.
- **Format:** CSV with columns: station_id, timestamp, rainfall_mm
- **Fixture:** `data/reference/imd_rainfall_fixture.csv`
- **Real integration:** Requires IMD credentials or data portal account

## SMAP Soil Moisture

- **Source:** NASA SMAP L3 Daily Soil Moisture
- **Access:** earthdata.nasa.gov account required
- **Format:** HDF5 or NetCDF, 9km or 36km resolution
- **Fixture:** Mock data in ingestion client
- **Real integration:** Requires NASA Earthdata credentials

## Bhuvan DEM / Susceptibility Layers

- **Source:** ISRO Bhuvan
- **Access:** Registration and approval required
- **Format:** GeoTIFF for DEM, WMS/WCS for layers
- **Fixture:** Sample SRTM/ASTER GDEM tile (clipped to pilot district)
- **Real integration:** Requires Bhuvan API access

## GSI Historical Landslide Inventory (Bhukosh)

- **Source:** Geological Survey of India Bhukosh portal
- **Access:** Web map viewer; bulk export not publicly documented
- **Format:** Point locations with dates (from published papers)
- **Fixture:** `data/reference/landslide_events.csv` curated from papers
- **Real integration:** Requires GSI MoU or published paper extraction

## Census / LGD Village Boundaries

- **Source:** Census of India / Local Government Directory
- **Access:** Publicly downloadable
- **Format:** Shapefile / GeoJSON
- **Usage:** Village-level risk zone polygons for pilot district
