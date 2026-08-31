"""SMS gateway interface.

Abstracts MSG91/Twilio behind SmsGatewayInterface so we can swap
providers without touching business logic.

Phase 0: Mock implementation that logs to console.
Phase 5: Real gateway integration.
"""

from abc import ABC, abstractmethod


class SmsGatewayInterface(ABC):
    @abstractmethod
    async def send_sms(
        self, phone_number: str, message: str, sender_id: str = ""
    ) -> dict:
        """Send an SMS to a phone number.

        Returns:
            dict with keys: success (bool), message_id (str), error (str|None).
        """
        ...


class MockSmsGateway(SmsGatewayInterface):
    """Mock SMS gateway for development and demo. Logs messages to console."""

    async def send_sms(
        self, phone_number: str, message: str, sender_id: str = ""
    ) -> dict:
        print(f"[MOCK SMS] To: {phone_number} | From: {sender_id} | Message: {message}")
        return {"success": True, "message_id": "mock-001", "error": None}
