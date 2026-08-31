from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NAME: str = "SIH26001 Landslide EWS"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/landslide_ews"
    )
    DATABASE_URL_SYNC: str = (
        "postgresql://postgres:postgres@localhost:5432/landslide_ews"
    )

    REDIS_URL: str = "redis://localhost:6379/0"

    JWT_SECRET_KEY: str = "CHANGE-ME-IN-PRODUCTION"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    SMS_GATEWAY_MOCK: bool = True
    SMS_GATEWAY_API_KEY: str = ""
    SMS_GATEWAY_SENDER_ID: str = ""

    FCM_CREDENTIALS_PATH: str = ""

    S3_ENDPOINT_URL: str = "http://localhost:9000"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_BUCKET_NAME: str = "landslide-reports"


settings = Settings()
