from typing import Dict, Any, Optional, Tuple
import requests
from requests import Response

from app.config import get_settings
from app.invoker_onboarding.invoker_capif_connector import onboard_invoker


class GatewayService:
    def __init__(self):
        self.settings = get_settings()
    
    def forward_request(
        self,
        method: str,
        target_url: str,
        params: Optional[Dict[str, str]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        access_token: Optional[str] = None
    ) -> Tuple[bytes, int, Optional[str]]:
        headers = {"Authorization": f"Bearer {access_token}"} if access_token else {}
        
        # Forward the request with the specified method and data
        resp: Response = requests.request(
            method=method,
            url=target_url,
            headers=headers,
            json=json_body,
            params=params
        )
        
        # Log the response body to console
        print(f"Response from {target_url}: {resp.text}")
        
        return resp.content, resp.status_code, resp.headers.get("Content-Type")
