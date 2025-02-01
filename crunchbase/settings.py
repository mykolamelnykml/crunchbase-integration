import enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(str, enum.Enum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    api_key: str = ""
    base_url: str = "https://api.crunchbase.com/v4/"

    api_delay: int = 1
    api_max_retry: int = 5

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="CRUNCHBASE_",
        env_file_encoding="utf-8",
    )


settings = Settings()
