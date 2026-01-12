from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv() 

class Settings(BaseSettings):
    """
    This class is to load the environment variables and use them in the application
    """

    app_name: str = "app"
    app_env: str = "development"
    log_level: str = "INFO"
    redis_host: str = os.getenv("REDIS_HOST", "redis")
    redis_port: int = os.getenv("REDIS_PORT", 6379)
    incoming_stream: str = os.getenv("INCOMING_STREAM", "chat:incoming")
    outgoing_stream: str = os.getenv("OUTGOING_STREAM", "chat:outgoing")
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "gpt-oss")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()