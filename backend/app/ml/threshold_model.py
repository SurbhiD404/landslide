def ne_himalaya_moisture_threshold(d_hours: float) -> float:
    """Published NE Himalaya moisture threshold.

    E(mm) = -11.10 + 0.62 * D(hr), valid for 24 < D < 1440 hr.

    Reference: NE-Himalaya rainfall-threshold research.

    Args:
        d_hours: Antecedent rainfall duration in hours.

    Returns:
        Threshold E in mm.

    Raises:
        ValueError: If d_hours is not in (24, 1440).
    """
    if not (24 < d_hours < 1440):
        raise ValueError(f"d_hours must be between 24 and 1440, got {d_hours}")
    return -11.10 + 0.62 * d_hours


def sikkim_intensity_duration_threshold(d_days: float) -> float:
    """Published Sikkim intensity-duration threshold.

    I = 43.26 * D^-0.78 (I in mm/day, D in days).

    Reference: NE-Himalaya rainfall-threshold research.

    Args:
        d_days: Duration in days.

    Returns:
        Threshold I in mm/day.
    """
    if d_days <= 0:
        raise ValueError(f"d_days must be positive, got {d_days}")
    return 43.26 * (d_days ** (-0.78))


def check_threshold_exceedance(
    cumulative_rainfall_mm: float,
    duration_hours: float,
    region: str = "ne_himalaya",
) -> dict:
    """Check whether rainfall exceeds the published threshold for a region.

    Args:
        cumulative_rainfall_mm: Total rainfall over the duration in mm.
        duration_hours: Duration of the rainfall event in hours.
        region: Which threshold to apply.

    Returns:
        dict with keys: exceeded (bool), threshold (float), actual (float), margin (float).
    """
    if region == "ne_himalaya":
        threshold = ne_himalaya_moisture_threshold(duration_hours)
        unit = "mm"
    elif region == "sikkim":
        d_days = duration_hours / 24.0
        threshold = sikkim_intensity_duration_threshold(d_days)
        unit = "mm/day"
    else:
        raise ValueError(f"Unknown region: {region}")

    exceeded = cumulative_rainfall_mm > threshold
    return {
        "exceeded": exceeded,
        "threshold": round(threshold, 2),
        "actual": cumulative_rainfall_mm,
        "unit": unit,
        "margin": round(cumulative_rainfall_mm - threshold, 2),
    }
