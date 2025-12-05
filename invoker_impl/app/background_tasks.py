"""Background tasks for the FastAPI application."""
import asyncio
from datetime import datetime
from app.invoker_onboarding.invoker_capif_connector import onboard_invoker
from app.utils.logger import get_app_logger

logger = get_app_logger(__name__)

jwt_token: str = None
last_updated: datetime = None

async def refresh_jwt_token():
    """Background task that refreshes JWT token every 9 minutes."""
    global jwt_token, last_updated
    
    while True:
        try:
            logger.info("Refreshing JWT token...")
            jwt_token = await asyncio.to_thread(onboard_invoker)
            last_updated = datetime.now()
            logger.info("JWT token refreshed successfully at %s", last_updated)
        except Exception as e:
            logger.error("Failed to refresh JWT token: %s", e)
        
        # Wait 9 minutes (540 seconds)
        await asyncio.sleep(540)

def get_jwt_token() -> str:
    if jwt_token is None:
        logger.warning("JWT token not yet initialized")
    return jwt_token
