from app.schemas.config_schema import ConfigurationCreateRequest, ConfigurationResponse
from app.services.storage_service import StorageService


class ConfigManager:
    """
    Handles configuration-level business logic for phase 2.
    """

    def __init__(self) -> None:
        self.storage_service = StorageService()

    def create_configuration(
        self, config_request: ConfigurationCreateRequest
    ) -> ConfigurationResponse:
        config_id = self.storage_service.generate_next_config_id()
        current_timestamp = self.storage_service.create_timestamp()

        config_data = {
            "config_id": config_id,
            "config_name": config_request.config_name,
            "document_type": config_request.document_type,
            "provider": config_request.provider,
            "model_name": config_request.model_name,
            "parameters": config_request.parameters.model_dump(),
            "fields": [field.model_dump() for field in config_request.fields],
            "created_at": current_timestamp,
            "updated_at": current_timestamp,
        }

        self.storage_service.save_configuration(config_data)

        return ConfigurationResponse(**config_data)

    def get_configuration(self, config_id: str) -> ConfigurationResponse:
        config_data = self.storage_service.load_configuration(config_id)
        return ConfigurationResponse(**config_data)

    def list_configurations(self) -> list[ConfigurationResponse]:
        configurations = self.storage_service.list_configurations()
        return [ConfigurationResponse(**config) for config in configurations]