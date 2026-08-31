"""Push notification gateway (Firebase Cloud Messaging).

Phase 0: Stub.
Phase 5: Real FCM integration.
"""


async def send_push_notification(user_id: int, title: str, body: str) -> dict:
    """Send a push notification to a user via FCM.

    Returns:
        dict with keys: success (bool), error (str|None).
    """
    return {"success": False, "error": "FCM not configured"}
