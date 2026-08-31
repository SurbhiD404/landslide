"""Alert rules engine.

When a zone's risk level crosses into High or Severe, automatically
create an alert record and dispatch it.

Phase 0: Stub with cooldown logic scaffolded.
Phase 5: Implement full rules + cooldown.
"""

ALERT_COOLDOWN_HOURS = 6


def should_dispatch_alert(
    zone_id: int, risk_level: str, last_alert_time: str | None
) -> dict:
    """Determine if an alert should be dispatched for a zone.

    Args:
        zone_id: The risk zone identifier.
        risk_level: Current risk level (Low/Moderate/High/Severe).
        last_alert_time: ISO timestamp of last alert for this zone, or None.

    Returns:
        dict with keys: should_dispatch (bool), reason (str).
    """
    if risk_level not in ("High", "Severe"):
        return {
            "should_dispatch": False,
            "reason": f"Risk level '{risk_level}' does not trigger alerts",
        }

    # TODO: Implement cooldown check against last_alert_time in Phase 5
    return {
        "should_dispatch": True,
        "reason": f"Risk level '{risk_level}' triggers alert dispatch",
    }
