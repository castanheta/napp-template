import os
from typing import Dict, Any, Optional, Tuple
import requests
from requests import Response

from app.invoker_onboarding.invoker_capif_connector import onboard_invoker


class GatewayService:
    
    def forward_request(
        self,
        method: str,
        target_url: str,
        params: Optional[Dict[str, str]] = None,
        json_body: Optional[Dict[str, Any]] = None
    ) -> Tuple[bytes, int, Optional[str]]:
        """
        Forward an HTTP request to the target URL with authorization.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            target_url: The destination URL to forward the request to
            params: Query parameters to include in the request
            json_body: JSON body for POST/PUT/PATCH requests
            
        Returns:
            Tuple of (response content, status code, content type)
        """
        # Onboard the invoker to get a fresh JWT token on each request
        try:
            access_token = onboard_invoker()
            print(f"Successfully onboarded invoker and obtained JWT token")
        except Exception as e:
            print(f"Warning: Failed to onboard invoker: {e}")
            # Fallback to environment variable if onboarding fails
            access_token = os.environ.get("ACCESS_TOKEN", "")
        
        headers = {"Authorization": f"Bearer {access_token}"}
        
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
