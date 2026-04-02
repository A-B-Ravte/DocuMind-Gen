from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import config_handling, doc_handling
from app.core.paths import STATIC_DIR, ensure_directories
from app.core.settings import settings


ensure_directories()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(config_handling.router)
app.include_router(doc_handling.router)


@app.get("/")
def root():
    return {"message": "DocuMind-Gen Phase 2 is running"}