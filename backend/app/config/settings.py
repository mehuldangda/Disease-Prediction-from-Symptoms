"""
Backend Settings Configuration using Pydantic Settings / Environment Variables.
"""

import os
from pydantic import BaseModel


class Settings(BaseModel):
    APP_NAME: str = "Disease Prediction API"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "*"
    ]
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "random_forest")


settings = Settings()
