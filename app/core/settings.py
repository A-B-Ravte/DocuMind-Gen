import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    """
    Central settings object for phase 2.
    Keep it simple for now.
    """

    def __init__(self) -> None:
        self.app_name: str = "DocuMind-Gen Phase 2"
        self.app_version: str = "2.0.0"

        self.google_api_key: str | None = os.getenv("GOOGLE_API_KEY")

        # Default server settings
        self.host: str = os.getenv("APP_HOST", "127.0.0.1")
        self.port: int = int(os.getenv("APP_PORT", "8000"))
        self.debug: bool = os.getenv("APP_DEBUG", "true").lower() == "true"

    def validate(self) -> None:
        """
        Validate required environment variables.
        Call this before invoking provider engines.
        """
        if not self.google_api_key:
            raise ValueError(
                "GOOGLE_API_KEY is not set. Please add it to your .env file."
            )


settings = Settings()