import os
from typing import Dict, Any, Optional, Tuple
import requests
from requests import Response
from opencapif_sdk import service_discoverer

from app.config import get_settings
from app.invoker_onboarding.invoker_capif_connector import (
    onboard_invoker, 
    refresh_token, 
    is_token_valid
)


class GatewayService:
    def __init__(self):
        self.settings = get_settings()
        self._access_token: Optional[str] = None
        self._service_discoverer: Optional[service_discoverer] = None
    
    def _ensure_valid_token(self) -> str:
        """
        Ensure we have a valid access token, refreshing or re-onboarding as needed.
        
        Returns:
            Valid JWT access token
            
        Raises:
            Exception if unable to obtain a valid token
        """
        # Check if we have a valid cached token
        if self._access_token and is_token_valid(self._access_token):
            print("Using cached valid token")
            return self._access_token
        
        # Try to refresh token if we have a discoverer instance
        if self._service_discoverer:
            try:
                print("Token expired or missing, refreshing...")
                self._access_token = refresh_token(self._service_discoverer)
                print("Successfully refreshed JWT token")
                return self._access_token
            except Exception as e:
                print(f"Warning: Token refresh failed: {e}. Attempting full onboarding...")
                self._service_discoverer = None
        
        # Full onboarding if no cached discoverer or refresh failed
        print("Performing full invoker onboarding...")
        self._access_token, self._service_discoverer = onboard_invoker()
        print("Successfully onboarded and obtained JWT token")
        return self._access_token
    
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
        # Ensure we have a valid token (using cache/refresh when possible)
        try:
            access_token = self._ensure_valid_token()
        except Exception as e:
            print(f"Error: Failed to obtain access token: {e}")
            raise
        
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
