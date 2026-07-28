from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Base Project Settings
    PROJECT_NAME: str = "AETHER-MIND Nexus Engine"
    ENVIRONMENT: str = "production"
    DEBUG: bool = False

    # Backblaze B2 Vault Configuration
    B2_KEY_ID: str = "your-b2-key-id"
    B2_APPLICATION_KEY: str = "your-b2-application-key"
    B2_BUCKET_NAME: str = "aether-telemetry-vault"

    # Telemetry & Resilience Settings
    CIRCUIT_FAILURE_THRESHOLD: int = 3
    CIRCUIT_RECOVERY_TIMEOUT: float = 10.0
    ANOMALY_Z_SCORE_THRESHOLD: float = 2.5

    # ✅ Pydantic V2 Clean Config (Zero Deprecation Warnings)
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


# ✅ Global Singleton Instance for clean imports across the engine
settings = Settings()