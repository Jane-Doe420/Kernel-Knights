import httpx
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import settings
from app.models.api_schemas import AgentResponse

logger = logging.getLogger(__name__)

class CallbackService:
    def __init__(self):
        self.url = settings.GUVI_CALLBACK_URL
        self.headers = {"Content-Type": "application/json"}

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def send_final_report(self, payload: dict):
        """
        Sends the mandatory final result to GUVI.
        Retries automatically on 5xx errors or network failures.
        """
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                logger.info(f"Sending callback for session {payload.get('sessionId')}")
                response = await client.post(
                    self.url,
                    json=payload,
                    headers=self.headers
                )
                response.raise_for_status()
                logger.info(f"Callback success: {response.status_code}")
                return True
            except httpx.HTTPStatusError as e:
                logger.error(f"Callback failed with status {e.response.status_code}: {e.response.text}")
                raise e
            except Exception as e:
                logger.error(f"Callback connection error: {str(e)}")
                raise e

callback_service = CallbackService()