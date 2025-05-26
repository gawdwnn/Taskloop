from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Configuration
    API_V1_PREFIX: str = ""
    PROJECT_NAME: str = ""
    DEBUG: bool = False

    # CORS
    BACKEND_CORS_ORIGINS: str = ""

    @property
    def cors_origins(self) -> List[str]:
        return [i.strip() for i in self.BACKEND_CORS_ORIGINS.split(",") if i.strip()]

    # Database Configuration
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    DATABASE_URL: str = ""

    # Redis Configuration
    REDIS_URL: str = ""

    # Security
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 0

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
