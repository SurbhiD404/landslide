# ML Data Pipeline Specification (ML-2)

## Overview

This document specifies the data and label pipeline for training the landslide risk classifier. The pipeline converts historical landslide inventory and spatial/temporal data into a training-ready dataset.

## Spatial Unit

**1km × 1km grid cells** (configurable via `PipelineConfig.grid_resolution_km`).

Each training sample is a `(grid_cell_id, sample_date)` pair.

Grid cells are identified by their centroid lat/lon (e.g., `"27.3200N_88.6100E"`).

## Labeling Methodology

### Positive Samples

A grid cell is a positive sample for a given event if:
1. The historical landslide point falls within the cell boundary.
2. The sample date matches the event date (or falls within the configurable `positive_window_days` window, defaulting to 0 = exact date only).

One positive sample per event (no duplicates from multiple landslides in the same cell on the same date).

### Negative Samples

Negative samples are grid cells that:
1. Are > `exclusion_buffer_km` (default 2km) from ANY historical landslide point.
2. Do not contain a known positive sample.
3. Are stratified by slope to match the positive sample distribution.

Sampling ratio: 1:N (default 1:3, configurable via `positive_negative_ratio`).

### Slope Stratification

Negative samples are distributed across slope bins to match the terrain diversity of positive samples:

1. Compute the slope distribution of positive samples across bins: [0-15°, 15-30°, 30-45°, 45-90°].
2. Allocate negatives proportionally: if 60% of positives are in 15-30°, then 60% of negatives come from cells with slope 15-30°.
3. This prevents the model from learning "flat = safe" instead of learning rainfall effects.

## Temporal Alignment

### Antecedent Features

All rainfall features use a **lookback window** that ends at `sample_date - 1`:

| Feature | Window |
|---------|--------|
| `rainfall_3d_mm` | Sum of daily rainfall from T-3 to T-1 |
| `rainfall_7d_mm` | Sum from T-7 to T-1 |
| `rainfall_15d_mm` | Sum from T-15 to T-1 |
| `rainfall_30d_mm` | Sum from T-30 to T-1 |

**Rainfall on the sample date itself is EXCLUDED** to prevent information leakage from the event day.

### Static Features

Slope, aspect, elevation, land cover, and road distance are computed once per grid cell and do not change over time.

## Leakage Prevention

| Check | Implementation |
|-------|---------------|
| No post-event features | Rainfall windows end at T-1, never T or after |
| No duplicate events | One positive sample per event_id |
| No train/test overlap | Time-based split: train < split_date, test ≥ split_date |
| No spatial leakage | Negatives excluded >2km from any landslide |
| No target-derived features | `distance_to_nearest_landslide` uses full inventory (acceptable as terrain susceptibility, not event-specific) |

## Output Schema

```
sample_id, grid_cell_id, centroid_lat, centroid_lon,
sample_date, event_date, label, risk_level, event_id,
source_reference, data_origin,
slope_angle_deg, slope_aspect_deg, elevation_m,
lulc_category, road_distance_km,
rainfall_3d_mm, rainfall_7d_mm, rainfall_15d_mm, rainfall_30d_mm
```

## Provenance Tracking

Every record includes `data_origin`:
- `"REAL"` — derived from actual historical data
- `"DEV_FIXTURE"` — synthetic data for pipeline testing only

**DEV_FIXTURE data must NEVER be used to report final ML performance.**

## Required Input Files

### 1. Landslide Inventory (BLOCKER)

`data/reference/landslide_events.csv`

```csv
event_id,event_date,latitude,longitude,severity,source_reference
```

### 2. Rainfall Time Series (BLOCKER)

`data/raw/rainfall_timeseries.csv`

```csv
station_id,station_lat,station_lon,reading_date,rainfall_mm
```

### 3. Static Features (Optional)

`data/reference/static_features.csv`

```csv
grid_cell_id,slope_angle_deg,slope_aspect_deg,elevation_m,lulc_category,road_distance_km
```

## Configuration

All parameters are in `PipelineConfig`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `grid_resolution_km` | 1.0 | Grid cell side length |
| `positive_window_days` | 0 | Days before event to include as positive |
| `exclusion_buffer_km` | 2.0 | Buffer around landslides for negative exclusion |
| `positive_negative_ratio` | 3 | Negative samples per positive |
| `slope_bins` | [0,15,30,45,90] | Slope bin boundaries for stratification |
| `train_test_split_date` | 2023-01-01 | Temporal split point |
| `data_origin` | "REAL" | Provenance label |
