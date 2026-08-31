# API Reference

Base URL: `http://localhost:8000/api/v1`

## Health

```
GET /health
```

Returns system health status.

## Risk Zones

```
GET /risk-zones
```

Return all risk zones with current risk level (GeoJSON).

```
GET /risk-zones/{zone_id}/history
```

Return risk trend over time for one zone.

```
GET /risk-zones/{zone_id}/explanation
```

Return human-readable explanation of why a zone is at its current risk level.

## Reports

```
POST /reports
```

Submit a citizen/field report (supports offline queue replay).

```
GET /reports?zone_id=&status=
```

List reports, optionally filtered by zone_id and status.

## Alerts

```
GET /alerts?district=&since=
```

Alert history, optionally filtered by district and timestamp.

```
POST /alerts/dispatch
```

Manually trigger an alert (admin override).

## Auth

```
POST /auth/login
```

Phone + OTP login. Returns JWT on success.

## Dashboard

```
GET /dashboard/summary
```

Aggregated stats: risk severity counts, road status, forecast.

## Weather

```
GET /weather/forecast?zone_id=
```

IMD-linked forecast for a zone.
