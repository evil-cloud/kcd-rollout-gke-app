from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "GitOps API"
    VERSION: str = "1.0.2"
    ROLLOUT_STRATEGY: str = "v1.0.5"
    EXTERNAL_API_URL: str = "https://jsonplaceholder.typicode.com/todos/1"
settings = Settings()
