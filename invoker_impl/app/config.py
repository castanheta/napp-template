import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    invoker_host: str = "127.0.0.1"
    invoker_port: int = 8000
    invoker_access_token_file: str = "./invoker_impl/invoker_folder/atnoguser/jwt_token.txt"
    invoker_config_file: str = "./app/invoker_onboarding/invoker_config_sample.json"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

def get_settings() -> Settings:
    return settings
