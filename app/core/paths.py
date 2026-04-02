from pathlib import Path


# Project root:
# app/core/paths.py -> core -> app -> project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

APP_DIR = BASE_DIR / "app"
DATA_DIR = BASE_DIR / "data"

CONFIGURATIONS_DIR = DATA_DIR / "configurations"
UPLOADS_DIR = DATA_DIR / "uploads"
OUTPUTS_DIR = DATA_DIR / "outputs"
EXECUTIONS_DIR = DATA_DIR / "executions"

TEMPLATES_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"


def ensure_directories() -> None:
    """
    Create all required runtime directories if they do not exist.
    Safe to call on startup.
    """
    required_dirs = [
        DATA_DIR,
        CONFIGURATIONS_DIR,
        UPLOADS_DIR,
        OUTPUTS_DIR,
        EXECUTIONS_DIR,
        TEMPLATES_DIR,
        STATIC_DIR,
    ]

    for directory in required_dirs:
        directory.mkdir(parents=True, exist_ok=True)