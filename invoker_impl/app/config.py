'''Configuration settings for the application using Pydantic.'''
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    invoker_host: str = "127.0.0.1"
    invoker_port: int = 8000
    invoker_access_token_file: str = "./invoker_impl/invoker_folder/atnoguser/jwt_token.txt"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

def get_settings() -> Settings:
    """
    Retrieve the current application settings.

    Returns:
        Settings: An instance containing the application's configuration settings.
    """
    return settings
