# Data Sources

## Current Status

**No real data is available.** All ingestion clients are stubs returning empty lists. The ML pipeline currently operates on synthetic DEV_FIXTURE data clearly marked as NOT REAL DATA.

---

## Data Sources Required

### 1. IMD Rainfall Data (BLOCKER)

- **Source:** India Meteorological Department
- **Access:** No public REST API. Requires institutional MoU or manual FTP download.
- **Format:** CSV with columns: `station_id, station_lat, station_lon, reading_date, rainfall_mm`
- **Usage:** Antecedent rainfall features (3d, 7d, 15d, 30d sums)
- **Status:** Stub only (`backend/app/ingestion/imd_client.py`)

### 2. GSI Historical Landslide Inventory / Bhukosh (BLOCKER)

- **Source:** Geological Survey of India Bhukosh portal
- **Access:** Web map viewer; bulk export not publicly documented
- **Format:** Point locations with dates (from published papers)
- **Usage:** Positive labels for ML training
- **Status:** Stub only (`backend/app/ingestion/gsi_client.py`)

### 3. SMAP Soil Moisture

- **Source:** NASA SMAP L3 Daily Soil Moisture
- **Access:** earthdata.nasa.gov account required
- **Format:** HDF5 or NetCDF, 9km or 36km resolution
- **Usage:** Static/semi-static feature for susceptibility
- **Status:** Stub only (`backend/app/ingestion/smap_client.py`)

### 4. Bhuvan DEM / Slope / Aspect

- **Source:** ISRO Bhuvan
- **Access:** Registration and approval required
- **Format:** GeoTIFF for DEM, WMS/WCS for layers
- **Usage:** Slope angle, aspect, elevation per grid cell
- **Status:** No client implemented

### 5. OpenStreetMap Road Network

- **Source:** OpenStreetMap
- **Access:** Publicly downloadable via Geofabrik
- **Format:** PBF / Shapefile
- **Usage:** Distance to nearest road per grid cell
- **Status:** No client implemented

### 6. Census / LGD Village Boundaries

- **Source:** Census of India / Local Government Directory
- **Access:** Publicly downloadable
- **Format:** Shapefile / GeoJSON
- **Usage:** Village-level risk zone polygons
- **Status:** No client implemented

---

## Dev Fixtures (Testing Only)

Synthetic data for pipeline verification. Must NEVER be used for final ML performance reporting.

| File | Description | Records |
|------|-------------|---------|
| `data/reference/landslide_events_dev_fixture.csv` | Synthetic landslide events | 10 |
| `data/raw/rainfall_dev_fixture.csv` | Synthetic daily rainfall | ~60 |

---

## Pipeline Input Files

The ML data pipeline (`backend/app/ml/data_pipeline.py`) reads:

| File | Required | Format |
|------|----------|--------|
| `data/reference/landslide_events.csv` | Yes | event_id, event_date, latitude, longitude, severity, source_reference |
| `data/raw/rainfall_timeseries.csv` | Yes | station_id, station_lat, station_lon, reading_date, rainfall_mm |
| `data/reference/static_features.csv` | Optional | grid_cell_id, slope_angle_deg, slope_aspect_deg, elevation_m, lulc_category, road_distance_km |
