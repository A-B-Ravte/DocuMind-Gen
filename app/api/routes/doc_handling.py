from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.constants import (
    DOCUMENT_STATUS_PENDING,
    EXECUTION_STATUS_CREATED,
)
from app.core.paths import TEMPLATES_DIR
from app.managers.config_manager import ConfigManager
from app.services.storage_service import StorageService

router = APIRouter(prefix="/docs", tags=["Documents"])
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

storage_service = StorageService()
config_manager = ConfigManager()


@router.get("/run", response_class=HTMLResponse)
def run_page(request: Request):
    configurations = config_manager.list_configurations()

    execution_summaries = []
    execution_files = sorted(
        Path(storage_service.get_execution_file_path("dummy")).parent.glob("*.json"),
        reverse=True,
    )

    for execution_file in execution_files:
        execution_data = storage_service._read_json_file(execution_file)
        execution_summaries.append(execution_data)

    return templates.TemplateResponse(
        "run.html",
        {
            "request": request,
            "configurations": configurations,
            "executions": execution_summaries,
            "page_title": "Run Extraction",
        },
    )


@router.post("/upload")
def upload_documents(
    config_id: str = Form(...),
    files: list[UploadFile] = File(...),
):
    try:
        config = config_manager.get_configuration(config_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    execution_id = storage_service.generate_next_execution_id()
    started_at = storage_service.create_timestamp()

    storage_service.create_execution_directories(execution_id)

    documents = []

    for index, uploaded_file in enumerate(files, start=1):
        if not uploaded_file.filename:
            continue

        saved_file_path = storage_service.save_uploaded_file(execution_id, uploaded_file)
        doc_id = storage_service.generate_document_id(index)

        document_info = {
            "doc_id": doc_id,
            "doc_name": uploaded_file.filename,
            "input_path": str(saved_file_path),
            "status": DOCUMENT_STATUS_PENDING,
            "result_json_path": None,
            "annotated_pdf_path": None,
            "error_message": None,
        }
        documents.append(document_info)

    if not documents:
        raise HTTPException(status_code=400, detail="No valid files were uploaded.")

    execution_data = {
        "execution_id": execution_id,
        "config_id": config.config_id,
        "config_name": config.config_name,
        "overall_status": EXECUTION_STATUS_CREATED,
        "documents": documents,
        "started_at": started_at,
        "completed_at": None,
    }

    storage_service.save_execution(execution_data)

    return {
        "message": "Documents uploaded successfully.",
        "execution_id": execution_id,
        "config_id": config.config_id,
        "uploaded_documents": documents,
    }


@router.get("/execution/{execution_id}")
def get_uploaded_execution(execution_id: str):
    try:
        return storage_service.load_execution(execution_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc