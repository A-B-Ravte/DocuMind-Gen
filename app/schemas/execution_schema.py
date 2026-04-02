from datetime import datetime
from pydantic import BaseModel, Field


class DocumentExecutionInfo(BaseModel):
    doc_id: str
    doc_name: str
    input_path: str
    status: str
    result_json_path: str | None = None
    annotated_pdf_path: str | None = None
    error_message: str | None = None


class ExecutionRunRequest(BaseModel):
    config_id: str = Field(..., min_length=1, description="Configuration ID to use for execution")
    uploaded_files: list[str] = Field(
        ...,
        min_length=1,
        description="List of uploaded file names or file paths associated with this execution"
    )


class ExecutionResponse(BaseModel):
    execution_id: str
    config_id: str
    config_name: str
    overall_status: str
    documents: list[DocumentExecutionInfo]
    started_at: datetime
    completed_at: datetime | None = None