"""Risk classifier — trains and predicts risk levels.

Planned approach (Phase 2):
    - Positive labels: historical_landslides table
    - Negative labels: stratified sampled non-landslide points
    - Model: XGBoost or RandomForest
    - Output: risk level (Low/Moderate/High/Severe) + probability

This module is a stub for Phase 0. Implement in Phase 2.
"""

RISK_LEVELS = ["Low", "Moderate", "High", "Severe"]


def predict_risk(features: dict) -> dict:
    """Stub prediction — returns Low risk until Phase 2 model is trained."""
    return {
        "risk_level": "Low",
        "confidence": 0.0,
        "model_version": "stub",
    }
