import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import UploadFile

from app.core.constants import CONFIG_ID_PREFIX, DOCUMENT_ID_PREFIX, EXECUTION_ID_PREFIX
from app.core.paths import CONFIGURATIONS_DIR, EXECUTIONS_DIR, OUTPUTS_DIR, UPLOADS_DIR


class StorageService:
    """
    Handles filesystem-based storage for phase 2.
    This includes:
    - config JSON files
    - execution JSON files
    - upload folders
    - output folders
    - incremental ID generation
    """

    @staticmethod
    def _read_json_file(file_path: Path) -> dict[str, Any]:
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def _write_json_file(file_path: Path, data: dict[str, Any]) -> None:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @staticmethod
    def _extract_numeric_part(file_name: str, prefix: str) -> int | None:
        """
        Example:
        config_001.json -> 1
        exec_012.json   -> 12
        """
        stem = Path(file_name).stem  # removes .json
        if not stem.startswith(f"{prefix}_"):
            return None

        numeric_part = stem.replace(f"{prefix}_", "", 1)
        if not numeric_part.isdigit():
            return None

        return int(numeric_part)

    def _generate_next_id(self, directory: Path, prefix: str) -> str:
        """
        Generates the next incrementing ID based on files already present.

        Example:
        existing: config_001.json, config_002.json
        next:     config_003
        """
        max_number = 0

        if directory.exists():
            for file_path in directory.iterdir():
                if file_path.is_file():
                    number = self._extract_numeric_part(file_path.name, prefix)
                    if number is not None and number > max_number:
                        max_number = number

        next_number = max_number + 1
        return f"{prefix}_{next_number:03d}"

    def generate_next_config_id(self) -> str:
        return self._generate_next_id(CONFIGURATIONS_DIR, CONFIG_ID_PREFIX)

    def generate_next_execution_id(self) -> str:
        return self._generate_next_id(EXECUTIONS_DIR, EXECUTION_ID_PREFIX)

    def generate_document_id(self, sequence_number: int) -> str:
        """
        Generates document ID within an execution.
        Example:
        1 -> doc_001
        2 -> doc_002
        """
        return f"{DOCUMENT_ID_PREFIX}_{sequence_number:03d}"

    def get_configuration_file_path(self, config_id: str) -> Path:
        return CONFIGURATIONS_DIR / f"{config_id}.json"

    def get_execution_file_path(self, execution_id: str) -> Path:
        return EXECUTIONS_DIR / f"{execution_id}.json"

    def get_upload_directory(self, execution_id: str) -> Path:
        return UPLOADS_DIR / execution_id

    def get_output_directory(self, execution_id: str) -> Path:
        return OUTPUTS_DIR / execution_id

    def get_document_output_directory(self, execution_id: str, doc_id: str) -> Path:
        return self.get_output_directory(execution_id) / doc_id

    def save_configuration(self, config_data: dict[str, Any]) -> Path:
        config_id = config_data["config_id"]
        file_path = self.get_configuration_file_path(config_id)
        self._write_json_file(file_path, config_data)
        return file_path

    def load_configuration(self, config_id: str) -> dict[str, Any]:
        file_path = self.get_configuration_file_path(config_id)
        if not file_path.exists():
            raise FileNotFoundError(f"Configuration not found for config_id: {config_id}")
        return self._read_json_file(file_path)

    def list_configurations(self) -> list[dict[str, Any]]:
        configurations: list[dict[str, Any]] = []

        if not CONFIGURATIONS_DIR.exists():
            return configurations

        for file_path in sorted(CONFIGURATIONS_DIR.glob("*.json")):
            configurations.append(self._read_json_file(file_path))

        return configurations

    def save_execution(self, execution_data: dict[str, Any]) -> Path:
        execution_id = execution_data["execution_id"]
        file_path = self.get_execution_file_path(execution_id)
        self._write_json_file(file_path, execution_data)
        return file_path

    def load_execution(self, execution_id: str) -> dict[str, Any]:
        file_path = self.get_execution_file_path(execution_id)
        if not file_path.exists():
            raise FileNotFoundError(f"Execution not found for execution_id: {execution_id}")
        return self._read_json_file(file_path)

    def save_result_json(
        self,
        execution_id: str,
        doc_id: str,
        result_data: dict[str, Any],
        file_name: str = "result.json",
    ) -> Path:
        doc_output_dir = self.get_document_output_directory(execution_id, doc_id)
        file_path = doc_output_dir / file_name
        self._write_json_file(file_path, result_data)
        return file_path

    def create_execution_directories(self, execution_id: str) -> tuple[Path, Path]:
        upload_dir = self.get_upload_directory(execution_id)
        output_dir = self.get_output_directory(execution_id)

        upload_dir.mkdir(parents=True, exist_ok=True)
        output_dir.mkdir(parents=True, exist_ok=True)

        return upload_dir, output_dir

    def create_document_output_directory(self, execution_id: str, doc_id: str) -> Path:
        doc_output_dir = self.get_document_output_directory(execution_id, doc_id)
        doc_output_dir.mkdir(parents=True, exist_ok=True)
        return doc_output_dir

    def save_uploaded_file(
        self,
        execution_id: str,
        uploaded_file: UploadFile,
    ) -> Path:
        upload_dir = self.get_upload_directory(execution_id)
        upload_dir.mkdir(parents=True, exist_ok=True)

        destination_path = upload_dir / uploaded_file.filename

        with destination_path.open("wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)

        return destination_path

    def create_timestamp(self) -> str:
        return datetime.now().isoformat()