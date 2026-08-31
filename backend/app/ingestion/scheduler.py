"""Celery beat scheduler configuration for periodic data ingestion.

This module configures scheduled tasks. Actual task implementations
are stubs until Phase 1.
"""

# Task schedule — will be imported by celery app configuration
INGESTION_SCHEDULE = {
    "imd-rainfall-every-3h": {
        "task": "app.ingestion.tasks.ingest_rainfall",
        "schedule": 10800.0,  # 3 hours in seconds
    },
    "soil-moisture-daily": {
        "task": "app.ingestion.tasks.ingest_soil_moisture",
        "schedule": 86400.0,  # 24 hours
    },
    "risk-recompute-daily": {
        "task": "app.ingestion.tasks.recompute_risk",
        "schedule": 86400.0,
    },
}
