from app.core.constants import (
    DOCUMENT_STATUS_COMPLETED,
    DOCUMENT_STATUS_FAILED,
    DOCUMENT_STATUS_PROCESSING,
    EXECUTION_STATUS_COMPLETED,
    EXECUTION_STATUS_FAILED,
    EXECUTION_STATUS_RUNNING,
)
from app.managers.framework import FrameworkManager
from app.services.storage_service import StorageService


class ExecutionManager:
    """
    Handles sync execution of uploaded documents for phase 2.
    """

    def __init__(self) -> None:
        self.storage_service = StorageService()
        self.framework_manager = FrameworkManager()

    def run_execution(self, execution_id: str) -> dict:
        execution_data = self.storage_service.load_execution(execution_id)
        config_data = self.storage_service.load_configuration(execution_data["config_id"])

        execution_data["overall_status"] = EXECUTION_STATUS_RUNNING
        self.storage_service.save_execution(execution_data)

        any_failures = False

        for document in execution_data["documents"]:
            try:
                document["status"] = DOCUMENT_STATUS_PROCESSING
                self.storage_service.save_execution(execution_data)

                process_result = self.framework_manager.process_document(
                    config_data=config_data,
                    execution_id=execution_id,
                    document_info=document,
                )

                document["status"] = DOCUMENT_STATUS_COMPLETED
                document["result_json_path"] = process_result["result_json_path"]
                document["annotated_pdf_path"] = process_result["annotated_pdf_path"]
                document["error_message"] = None

                self.storage_service.save_execution(execution_data)

            except Exception as exc:
                any_failures = True
                document["status"] = DOCUMENT_STATUS_FAILED
                document["error_message"] = str(exc)
                self.storage_service.save_execution(execution_data)

        execution_data["overall_status"] = (
            EXECUTION_STATUS_FAILED if any_failures else EXECUTION_STATUS_COMPLETED
        )
        execution_data["completed_at"] = self.storage_service.create_timestamp()

        self.storage_service.save_execution(execution_data)
        return execution_data

    def get_execution(self, execution_id: str) -> dict:
        return self.storage_service.load_execution(execution_id)

    def get_execution_result(self, execution_id: str) -> list[dict]:
        execution_data = self.storage_service.load_execution(execution_id)
        results = []

        for document in execution_data["documents"]:
            result_json_path = document.get("result_json_path")
            if result_json_path:
                result_data = self.storage_service._read_json_file(result_json_path)
                results.append(result_data)

        return results