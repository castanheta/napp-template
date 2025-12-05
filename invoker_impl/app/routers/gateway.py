"""Gateway router for forwarding HTTP requests."""
from fastapi import APIRouter, Query, Request, HTTPException
from fastapi.responses import Response as FastAPIResponse

from app.services import GatewayService
from app.background_tasks import get_jwt_token

router = APIRouter(tags=["gateway"])
gateway_service = GatewayService()


@router.api_route("/forward", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def forward_request(
    target_url: str = Query(..., description="The target URL to forward the request to"),
    request: Request = None
) -> FastAPIResponse:
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
    
    # Get JWT token from background task
    jwt_token = get_jwt_token()
    if not jwt_token:
        raise HTTPException(status_code=503, detail="JWT token not available yet")
    
    try:
        content, status_code, content_type = gateway_service.forward_request(
            method=request.method,
            target_url=target_url,
            params=params if params else None,
            json_body=json_body,
            access_token=jwt_token
        )
        return FastAPIResponse(
            content=content,
            status_code=status_code,
            media_type=content_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error forwarding request: {str(e)}")
