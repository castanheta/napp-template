"""Schema definitions for gateway endpoints."""
from typing import Optional, Dict, Any
from pydantic import BaseModel, HttpUrl


class ForwardRequest(BaseModel):
    """Request model for forwarding HTTP requests."""
    target_url: HttpUrl
    params: Optional[Dict[str, str]] = None
    json_body: Optional[Dict[str, Any]] = None


class ForwardResponse(BaseModel):
    """Response model for forwarded requests."""
    content: Any
    status_code: int
    content_type: Optional[str] = None
