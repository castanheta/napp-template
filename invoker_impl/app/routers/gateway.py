"""Gateway router for forwarding HTTP requests."""
from fastapi import APIRouter, Query, Request, HTTPException
from fastapi.responses import Response as FastAPIResponse

from app.services import GatewayService

router = APIRouter(tags=["gateway"])
gateway_service = GatewayService()


@router.api_route("/forward", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def forward_request(
    target_url: str = Query(..., description="The target URL to forward the request to"),
    request: Request = None
) -> FastAPIResponse:
    """
    Forward an HTTP request to the target URL with any method.
    
    Supports: GET, POST, PUT, DELETE, PATCH
    
    Args:
        target_url: The destination URL to forward the request to
        request: The incoming FastAPI request object
        
    Returns:
        Response from the target URL with the same status code and content type
    """
    # Extract additional query parameters (excluding target_url)
    params = dict(request.query_params)
    params.pop("target_url", None)
    
    # Get JSON body if present (for POST, PUT, PATCH)
    json_body = None
    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            json_body = await request.json()
        except:
            json_body = None
    
    try:
        content, status_code, content_type = gateway_service.forward_request(
            method=request.method,
            target_url=target_url,
            params=params if params else None,
            json_body=json_body
        )
        return FastAPIResponse(
            content=content,
            status_code=status_code,
            media_type=content_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error forwarding request: {str(e)}")
