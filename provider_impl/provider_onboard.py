import os
import logging
from pathlib import Path
from opencapif_sdk import capif_provider_connector, api_schema_translator

logger = logging.getLogger(__name__)

CAPIF_DIR = Path(__file__).parent

CAPIF_ENABLED = os.getenv("CAPIF_ENABLED", "true").lower() == "true"

PROVIDER_API_HOST = os.getenv("PROVIDER_API_HOST", "10.255.32.133")
PROVIDER_API_PORT = os.getenv("PROVIDER_API_PORT", "8000")
PROVIDER_CONFIG_FILE = os.getenv("PROVIDER_CONFIG_FILE", "./provider_config_sample.json")
PROVIDER_OPENAPI_FILE = os.getenv("PROVIDER_OPENAPI_FILE", "./openapi.yaml")
PROVIDER_API_DESC_FILE = os.getenv("PROVIDER_API_DESC_FILE", "./slice-manager5.json")

API_URL = f"https://{PROVIDER_API_HOST}:{PROVIDER_API_PORT}/slice-manager5/v1"


def run_capif_onboarding() -> None:
    if not CAPIF_ENABLED:
        logger.info("CAPIF_ENABLED=false, skipping provider onboarding.")
        return

    logger.info("Starting CAPIF provider onboarding...")
    try:
        capif_connector = capif_provider_connector(config_file=PROVIDER_CONFIG_FILE)

        capif_connector.onboard_provider()

        translator = api_schema_translator(PROVIDER_OPENAPI_FILE)
        translator.build(API_URL, "0", "0")

        capif_connector.api_description_path = PROVIDER_API_DESC_FILE
        apf = capif_connector.provider_capif_ids["APF-1"]
        aef = capif_connector.provider_capif_ids["AEF-1"]

        capif_connector.publish_req["publisher_apf_id"] = apf
        capif_connector.publish_req["publisher_aefs_ids"] = [aef]
        capif_connector.supported_features = "0"

        capif_connector.publish_services()
        logger.info("CAPIF provider onboarding completed successfully.")
    except Exception as exc:
        logger.exception("CAPIF provider onboarding failed: %s", exc)
        raise

if __name__ == "__main__":
    run_capif_onboarding()