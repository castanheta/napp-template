import os
from opencapif_sdk import capif_invoker_connector,service_discoverer
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

def onboard_invoker() -> str:
    """
    Onboards an invoker to the CAPIF system, discovers available services, retrieves a JWT access token, 
    prints it, and writes it to a file.
    This function performs the following steps:
    1. Initializes the CAPIF invoker connector using the provided configuration file.
    2. Onboards the invoker to the CAPIF system.
    3. Initializes the service discoverer using the same configuration file.
    4. Discovers available services.
    5. Retrieves JWT tokens from the service discoverer.
    6. Prints the obtained JWT token.
    7. Writes the JWT token to a specified access token file.

    Raises:
        Any exceptions raised by the underlying connector or file operations.
    """

    capif_connector = capif_invoker_connector(config_file=settings.invoker_config_file)

    capif_connector.onboard_invoker()

    discoverer_svc = service_discoverer(config_file=settings.invoker_config_file)
    discoverer_svc.discover()


    discoverer_svc.get_tokens()
    jwt_token=discoverer_svc.token

    return jwt_token

    # print("JWT TOKEN: ", jwt_token)

    # _write_to_file(settings.invoker_access_token_file, jwt_token)
