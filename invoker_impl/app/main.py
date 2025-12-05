""""Main entry point for the FastAPI application.
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

from app.routers import gateway_router
from app.config import get_settings
from app.utils.logger import get_app_logger
#from app.utils.http_callback_server import callback_app
from app.background_tasks import refresh_jwt_token

settings = get_settings()

logger = get_app_logger(__name__)
logger.info("Starting INVOKER APP")
logger.info("Host: %s, Port: %s", settings.invoker_host, settings.invoker_port)
logger.info("Log Directory Path: %s", settings.invoker_log_directory_path)
logger.info("Log Filename Path: %s", settings.invoker_log_filename_path)
logger.info("Provider Target URL: %s", settings.provider_target_url)
logger.info("Invoker Access Token File: %s", settings.invoker_access_token_file)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting JWT token refresh background task")
    task = asyncio.create_task(refresh_jwt_token())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        logger.info("JWT token refresh task cancelled")


app = FastAPI(lifespan=lifespan)
app.include_router(gateway_router.router, prefix="/gateway")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.invoker_host, port=settings.invoker_port)
