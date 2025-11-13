""""Main entry point for the FastAPI application.
"""
from fastapi import FastAPI
from app.config import get_settings
from app.routers import gateway_router

settings = get_settings()

app = FastAPI(
    title="Invoker Gateway API",
    description="API for forwarding requests with authentication",
    version="1.0.0"
)

# Include the gateway router
app.include_router(gateway_router, prefix="/gateway", tags=["gateway"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.invoker_host, port=settings.invoker_port)
