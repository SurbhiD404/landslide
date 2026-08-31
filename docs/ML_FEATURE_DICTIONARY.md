# Feature Dictionary (ML-3)

## Overview

This document describes all features computed by the ML-3 feature engineering pipeline. Each feature includes its definition, units, source, calculation method, spatial/temporal resolution, missing-value handling, and leakage considerations.

## Feature Summary

| Feature | Family | Availability | Missing Value |
|---------|--------|-------------|---------------|
| `rainfall_current_mm` | Rainfall | DEV_FIXTURE_ONLY | 0.0 |
| `rainfall_3d_mm` | Rainfall | DEV_FIXTURE_ONLY | 0.0 |
| `rainfall_7d_mm` | Rainfall | DEV_FIXTURE_ONLY | 0.0 |
| `rainfall_15d_mm` | Rainfall | DEV_FIXTURE_ONLY | 0.0 |
| `rainfall_30d_mm` | Rainfall | DEV_FIXTURE_ONLY | 0.0 |
| `slope_angle_deg` | Terrain | DEV_FIXTURE_ONLY | 0.0 |
| `slope_aspect_deg` | Terrain | DEV_FIXTURE_ONLY | 0.0 |
| `elevation_m` | Terrain | DEV_FIXTURE_ONLY | 0.0 |
| `distance_nearest_landslide_km` | Proximity | DEV_FIXTURE_ONLY | 999.0 |
| `n_landslides_within_5km` | Proximity | DEV_FIXTURE_ONLY | 0 |
| `lulc_category` | Land Cover | UNAVAILABLE | 0 |
| `road_distance_km` | Road | UNAVAILABLE | 999.0 |

---

## Feature Definitions

### Rainfall Features

#### `rainfall_current_mm`
- **Description**: Rainfall on the day immediately before the sample date (T-1)
- **Units**: mm
- **Source**: IMD daily rainfall
- **Calculation**: Nearest-station daily rainfall on day T-1
- **Spatial Resolution**: Station-level (point data, not gridded)
- **Temporal Resolution**: Daily
- **Missing Value**: 0.0 if no station within range or no data available
- **Leakage Notes**: Excludes sample date; uses only T-1 data

#### `rainfall_3d_mm`
- **Description**: Sum of daily rainfall from T-3 to T-1
- **Units**: mm
- **Source**: IMD daily rainfall
- **Calculation**: Sum of nearest-station daily rainfall over [3 days ending T-1]
- **Spatial Resolution**: Station-level
- **Temporal Resolution**: Daily
- **Missing Value**: 0.0 if no station within range
- **Leakage Notes**: Excludes sample date; uses only data from T-3 to T-1

#### `rainfall_7d_mm`
- **Description**: Sum of daily rainfall from T-7 to T-1
- **Units**: mm
- **Source**: IMD daily rainfall
- **Calculation**: Sum of nearest-station daily rainfall over [7 days ending T-1]
- **Missing Value**: 0.0 if no station within range
- **Leakage Notes**: Excludes sample date

#### `rainfall_15d_mm`
- **Description**: Sum of daily rainfall from T-15 to T-1
- **Units**: mm
- **Source**: IMD daily rainfall
- **Missing Value**: 0.0 if no station within range
- **Leakage Notes**: Excludes sample date

#### `rainfall_30d_mm`
- **Description**: Sum of daily rainfall from T-30 to T-1
- **Units**: mm
- **Source**: IMD daily rainfall
- **Missing Value**: 0.0 if no station within range
- **Leakage Notes**: Excludes sample date

---

### Terrain Features

#### `slope_angle_deg`
- **Description**: Terrain slope angle derived from DEM
- **Units**: degrees
- **Source**: DEM (Bhuvan/SRTM) — currently DEV_FIXTURE
- **Calculation**: 3x3 window slope from DEM (Horn's method)
- **Spatial Resolution**: Same as DEM (30m, resampled to grid)
- **Temporal Resolution**: Static (time-invariant)
- **Missing Value**: 0.0 if DEM data unavailable
- **Leakage Notes**: Static feature — no temporal component
- **DEM Processing**: See `backend/app/ml/terrain_dem.py` for methodology

#### `slope_aspect_deg`
- **Description**: Terrain slope aspect derived from DEM
- **Units**: degrees (0=N, 90=E, 180=S, 270=W)
- **Source**: DEM — currently DEV_FIXTURE
- **Calculation**: 3x3 window aspect from DEM
- **Missing Value**: 0.0 if DEM data unavailable
- **Leakage Notes**: Static feature — no temporal component

#### `elevation_m`
- **Description**: Terrain elevation at grid cell centroid
- **Units**: meters
- **Source**: DEM — currently DEV_FIXTURE
- **Calculation**: Bilinear interpolation at cell centroid
- **Missing Value**: 0.0 if DEM data unavailable
- **Leakage Notes**: Static feature — no temporal component

---

### Proximity Features

#### `distance_nearest_landslide_km`
- **Description**: Distance from grid cell centroid to nearest historical landslide
- **Units**: km
- **Source**: Landslide inventory (GSI/curated papers)
- **Calculation**: Haversine distance to nearest event with `event_date < sample_date`
- **Spatial Resolution**: 1km grid cell centroid
- **Temporal Resolution**: Computed per sample_date (uses only past events)
- **Missing Value**: 999.0 if no historical landslides exist before sample_date
- **Leakage Notes**: **CRITICAL** — Only uses events with `event_date < sample_date`. For a positive sample, the target event itself is excluded.

#### `n_landslides_within_5km`
- **Description**: Count of historical landslides within 5km of grid cell
- **Units**: count
- **Source**: Landslide inventory
- **Calculation**: Count of events with `event_date < sample_date` and `distance < 5km`
- **Missing Value**: 0 if no historical landslides exist before sample_date
- **Leakage Notes**: **CRITICAL** — Only uses events with `event_date < sample_date`

---

### Land Cover Features (UNAVAILABLE)

#### `lulc_category`
- **Description**: Land use / land cover category
- **Units**: categorical integer
- **Source**: Land cover dataset (to be determined)
- **Calculation**: Majority class within grid cell from land cover raster
- **Missing Value**: 0 (unknown) — NOT fabricated
- **Status**: **UNAVAILABLE** — no real dataset identified
- **Action Required**: Identify and obtain a documented land cover dataset for NER region

---

### Road Features (UNAVAILABLE)

#### `road_distance_km`
- **Description**: Distance to nearest road
- **Units**: km
- **Source**: OpenStreetMap road network
- **Calculation**: Nearest road segment distance from cell centroid
- **Missing Value**: 999.0 (unknown) — NOT fabricated
- **Status**: **UNAVAILABLE** — no road dataset loaded
- **Action Required**: Download OSM road network for NER region, compute nearest-road distances

---

## Leakage Prevention Summary

| Check | Status | Implementation |
|-------|--------|----------------|
| Future rainfall leakage | PREVENTED | All rainfall features use [T-window, T-1], never T or after |
| Post-event information | PREVENTED | Antecedent rainfall excludes sample date |
| Target-event proximity | PREVENTED | `exclude_event_id` parameter removes target from proximity computation |
| Train/test contamination | PREVENTED | Time-based split at configurable date |
| Duplicate samples | PREVENTED | One positive per event_id |
| Label-derived features | PREVENTED | No features use the label as input |

---

## Data Provenance

All feature values carry a `data_origin` field:
- `"REAL"` — derived from actual historical data
- `"DEV_FIXTURE"` — synthetic data for pipeline testing only

**DEV_FIXTURE data must NEVER be used to report final ML performance.**

---

## Feature Availability Matrix

| Feature | Real Data | Dev Fixture | Pipeline Ready |
|---------|-----------|-------------|----------------|
| rainfall_current_mm | ❌ | ✅ | ✅ |
| rainfall_3d_mm | ❌ | ✅ | ✅ |
| rainfall_7d_mm | ❌ | ✅ | ✅ |
| rainfall_15d_mm | ❌ | ✅ | ✅ |
| rainfall_30d_mm | ❌ | ✅ | ✅ |
| slope_angle_deg | ❌ | ✅ | ✅ |
| slope_aspect_deg | ❌ | ✅ | ✅ |
| elevation_m | ❌ | ✅ | ✅ |
| distance_nearest_landslide_km | ❌ | ✅ | ✅ |
| n_landslides_within_5km | ❌ | ✅ | ✅ |
| lulc_category | ❌ | ❌ | ✅ (stub) |
| road_distance_km | ❌ | ❌ | ✅ (stub) |
