import os
import sys
from datetime import datetime, timedelta
from typing import Optional, Tuple
import jwt
from opencapif_sdk import capif_invoker_connector,service_discoverer

# Add parent directory to path when running as standalone script
if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.config import get_settings

# Deprecated: Environment variables now managed centrally via config.py
# INVOKER_CONFIG_FILE = os.getenv('INVOKER_CONFIG_FILE', 'invoker_config_sample.json')
# INVOKER_ACCESS_TOKEN_FILE = os.getenv('INVOKER_ACCESS_TOKEN_FILE', 'app/invoker_folder/atnoguser/jwt_token.txt')

settings = get_settings()

def _write_to_file(filename, content):
    if os.path.exists(filename):
        os.remove(filename)

    with open(filename, "w", encoding='utf-8') as f:
        f.write(content)
    print(f"Wrote content to {filename}")

def get_token_expiration(token: str) -> Optional[datetime]:
    """
    Extract expiration time from JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        Expiration datetime or None if unable to decode
    """
    try:
        # Decode without verification to read expiration
        decoded = jwt.decode(token, options={"verify_signature": False})
        exp_timestamp = decoded.get('exp')
        if exp_timestamp:
            return datetime.fromtimestamp(exp_timestamp)
    except Exception as e:
        print(f"Warning: Could not decode token expiration: {e}")
    return None


def is_token_valid(token: str, buffer_seconds: int = 60) -> bool:
    """
    Check if a JWT token is still valid with a buffer time.
    
    Args:
        token: JWT token string
        buffer_seconds: Seconds before expiration to consider token invalid (default 60)
        
    Returns:
        True if token is valid and not expiring soon, False otherwise
    """
    if not token:
        return False
    
    expiration = get_token_expiration(token)
    if not expiration:
        return False
    
    # Consider token invalid if it expires within buffer_seconds
    return datetime.now() + timedelta(seconds=buffer_seconds) < expiration


def refresh_token(discoverer: service_discoverer) -> str:
    """
    Refresh JWT token using existing service_discoverer instance.
    
    Args:
        discoverer: Existing service_discoverer instance
        
    Returns:
        New JWT token string
        
    Raises:
        Any exceptions raised by the token refresh operation
    """
    discoverer.get_tokens()
    return discoverer.token


def onboard_invoker() -> Tuple[str, service_discoverer]:
    """
    Onboards an invoker to the CAPIF system, discovers available services, and retrieves a JWT access token.
    
    This function performs the following steps:
    1. Initializes the CAPIF invoker connector using the provided configuration file.
    2. Onboards the invoker to the CAPIF system.
    3. Initializes the service discoverer using the same configuration file.
    4. Discovers available services.
    5. Retrieves JWT tokens from the service discoverer.
    
    Returns:
        Tuple of (JWT token string, service_discoverer instance)

    Raises:
        Any exceptions raised by the underlying connector or operations.
    """

    capif_connector = capif_invoker_connector(config_file=settings.invoker_config_file)

    capif_connector.onboard_invoker()

    discoverer_svc = service_discoverer(config_file=settings.invoker_config_file)
    discoverer_svc.discover()

    discoverer_svc.get_tokens()
    jwt_token = discoverer_svc.token

    return jwt_token, discoverer_svc

if __name__ == "__main__":
    print("Starting invoker onboarding process...")
    token, discoverer = onboard_invoker()
    print(f"JWT TOKEN: {token}")
    print(f"Token valid: {is_token_valid(token)}")
    if expiration := get_token_expiration(token):
        print(f"Token expires at: {expiration}")
    print("Invoker onboarding completed successfully!")
