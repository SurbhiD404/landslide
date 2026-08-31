# Demo Script — End-to-End Walkthrough

## Pre-Demo Checklist

1. Docker Compose running (`docker compose up -d`)
2. Backend healthy (`curl http://localhost:8000/health`)
3. Dashboard loaded at `http://localhost:5173`
4. Field PWA loaded at `http://localhost:5174`
5. Mock SMS log accessible (console output)

## Demo Flow

### Step 1: Show Current Risk State
- Open dashboard → navigate to risk zone map
- Show all zones at Low risk (initial state)
- Point out the zone explanation panel

### Step 2: Simulate Rainfall Spike
- Call the backend API to inject rainfall data for a zone:
  ```
  POST /api/v1/weather/simulate-rainfall
  { "zone_id": 1, "rainfall_mm": 210, "duration_hours": 72 }
  ```
- Or trigger the risk recomputation manually

### Step 3: Risk Recomputation
- Show the risk engine evaluating the zone against published thresholds
- Display the threshold equation: E = -11.10 + 0.62 * D
- Show the actual vs threshold comparison

### Step 4: Risk Level Change
- Dashboard updates: zone changes from Low → High/Severe
- Color-coded heatmap reflects new risk level

### Step 5: Alert Dispatch
- Alert created with human-readable explanation
- SMS dispatched (mock: logged to console with multilingual template)
- Push notification sent via FCM (if configured)

### Step 6: Field Report
- Open field PWA → submit a report (photo + description)
- Report appears in dashboard alert console

### Step 7: Judge Q&A Preparation
- "Why threshold + ML?" — Explainable alerts; district officers can see WHY
- "How is this different from LANDSLIP?" — NER is planned, not active; we fill the gap
- "How do we trust AI alerts?" — Every alert shows the threshold comparison

## Fallback Demo
If network issues arise at venue, run the pre-recorded demo video (record by Day 14 EOD).
