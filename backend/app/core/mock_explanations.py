from typing import TypedDict


class ExplanationData(TypedDict):
    explanation: str
    thresholds: list[dict]


EXPLANATIONS: dict[str, ExplanationData] = {
    "Low": {
        "explanation": "72-hr cumulative rainfall of 28mm is below this zone's regional threshold of 120mm (NE Himalaya moisture threshold).",
        "thresholds": [
            {"name": "NE Himalaya moisture threshold (72hr)", "threshold_value": 120, "actual_value": 28},
        ],
    },
    "Moderate": {
        "explanation": "72-hr cumulative rainfall of 142mm exceeds this zone's regional threshold of 120mm but remains below the high-risk threshold of 180mm (NE Himalaya moisture threshold).",
        "thresholds": [
            {"name": "NE Himalaya moisture threshold (72hr)", "threshold_value": 120, "actual_value": 142},
        ],
    },
    "High": {
        "explanation": "72-hr cumulative rainfall of 205mm exceeds this zone's high-risk threshold of 180mm (NE Himalaya moisture threshold) and approaches severe levels.",
        "thresholds": [
            {"name": "NE Himalaya moisture threshold (72hr) - high", "threshold_value": 180, "actual_value": 205},
        ],
    },
    "Severe": {
        "explanation": "72-hr cumulative rainfall of 245mm exceeds this zone's regional threshold of 180mm (NE Himalaya moisture threshold) by a wide margin.",
        "thresholds": [
            {"name": "NE Himalaya moisture threshold (72hr) - severe", "threshold_value": 180, "actual_value": 245},
        ],
    },
}


def get_explanation_for_risk_level(risk_level: str) -> ExplanationData:
    """Get mock explanation data for a given risk level."""
    return EXPLANATIONS.get(risk_level, EXPLANATIONS["Low"])