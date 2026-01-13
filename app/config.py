from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    BROKER_URL: str

    CACHE_HOST: str
    CACHE_PORT: int

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()