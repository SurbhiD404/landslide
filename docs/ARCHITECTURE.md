# Architecture

## System Overview

A cloud-hosted, offline-tolerant platform that fuses rainfall/soil-moisture/terrain/satellite data with published NE-Himalaya rainfall-threshold research to classify landslide risk by zone, push multilingual alerts to district administrations and citizens, and let field officials/citizens report ground-truth hazards via geo-tagged photo uploads.

## User Classes

- **District Disaster Management Authorities** — risk dashboard, alert dispatch, road connectivity
- **Field officials / citizens** — lightweight PWA, offline-first reporting, SMS alerts
- **System/ML pipeline** — data ingestion, risk recomputation, alert triggers

## Data Flow

```mermaid
flowchart TB
    subgraph External["External Data Sources"]
        IMD["IMD Rainfall Data"]
        SMAP["SMAP/ESA CCI Soil Moisture"]
        BHUVAN["Bhuvan DEM & Susceptibility Layers"]
        GSI["GSI Landslide Inventory"]
    end

    subgraph Ingestion["Data Ingestion Layer"]
        SCHED["Scheduled Jobs (Celery Beat)"]
        ETL["ETL Workers (Python)"]
    end

    subgraph Core["Core Backend (FastAPI)"]
        API["REST API"]
        RISK["Risk Engine: Threshold Model + ML Classifier"]
        ALERT["Alert Dispatcher (rules engine)"]
        AUTH["Auth Service (JWT)"]
    end

    subgraph Data["Data Layer"]
        PG["PostgreSQL + PostGIS"]
        REDIS["Redis (cache, queues)"]
        S3["Object Storage (MinIO/S3)"]
    end

    subgraph Clients["Client Applications"]
        WEB["React + Leaflet GIS Dashboard"]
        PWA["Offline-first PWA"]
    end

    subgraph Notify["Notification Layer"]
        SMS["SMS Gateway"]
        PUSH["Push Notifications (FCM)"]
    end

    IMD --> SCHED
    SMAP --> SCHED
    BHUVAN --> SCHED
    GSI --> SCHED
    SCHED --> ETL --> PG
    PG --> RISK --> PG
    RISK --> ALERT --> SMS
    ALERT --> PUSH
    API --> PG
    API --> REDIS
    API --> S3
    WEB --> API
    PWA --> API
```

## Tech Stack

| Layer | Choice |
|-------|--------|
| Backend | Python 3.11 + FastAPI |
| ML | scikit-learn / XGBoost |
| Database | PostgreSQL + PostGIS |
| Cache/Queue | Redis + Celery |
| Object Storage | MinIO (local) / AWS S3 |
| Dashboard | React + TypeScript + Leaflet.js |
| Field App | React PWA with Workbox |
| Notifications | MSG91/Twilio (SMS) + FCM (push) |
| CI/CD | GitHub Actions |
| Infra | Docker Compose (local) |

## Differentiation

This system applies NE-Himalaya-specific rainfall thresholds from peer-reviewed research to close the regional coverage gap left by GSI's LANDSLIP system (NER is a planned, not yet active, expansion state). It adds a citizen-reporting layer that GSI's system lacks.
