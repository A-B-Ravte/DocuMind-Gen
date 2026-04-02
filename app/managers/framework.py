import json
from pathlib import Path

from app.core.constants import RESULT_JSON_FILENAME
from app.engines.gemini import GeminiEngine
from app.managers.prompt_manager import PromptManager
from app.services.annotation_service import AnnotationService
from app.services.storage_service import StorageService


class FrameworkManager:
    """
    Orchestrates one document extraction flow:
    config -> prompt -> Gemini -> result JSON -> annotation
    """

    def __init__(self) -> None:
        self.storage_service = StorageService()
        self.prompt_manager = PromptManager()
        self.annotation_service = AnnotationService()
        self.gemini_engine = GeminiEngine()

    def process_document(
        self,
        config_data: dict,
        execution_id: str,
        document_info: dict,
    ) -> dict:
        doc_id = document_info["doc_id"]
        doc_name = document_info["doc_name"]
        input_path = document_info["input_path"]

        prompt = self.prompt_manager.build_extraction_prompt(config_data)

        raw_response = self.gemini_engine.extract_from_pdf(
            pdf_path=input_path,
            prompt=prompt,
            model_name=config_data["model_name"],
            parameters=config_data["parameters"],
        )

        extracted_data = json.loads(raw_response)

        result_payload = {
            "doc_id": doc_id,
            "doc_name": doc_name,
            "config_id": config_data["config_id"],
            "provider": config_data["provider"],
            "model_name": config_data["model_name"],
            "extracted_data": extracted_data,
            "generated_at": self.storage_service.create_timestamp(),
        }

        result_json_path = self.storage_service.save_result_json(
            execution_id=execution_id,
            doc_id=doc_id,
            result_data=result_payload,
            file_name=RESULT_JSON_FILENAME,
        )

        doc_output_dir = self.storage_service.create_document_output_directory(
            execution_id=execution_id,
            doc_id=doc_id,
        )

        annotated_pdf_path = self.annotation_service.create_annotated_pdf(
            input_pdf_path=input_path,
            extracted_data=extracted_data,
            output_dir=doc_output_dir,
        )

        return {
            "result_json_path": str(result_json_path),
            "annotated_pdf_path": str(annotated_pdf_path),
            "result_payload": result_payload,
        }