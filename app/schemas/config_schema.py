from datetime import datetime
from pydantic import BaseModel, Field, field_validator

from app.core.constants import DEFAULT_MODEL_NAME, DEFAULT_PROVIDER, SUPPORTED_PROVIDERS


class FieldConfig(BaseModel):
    field_name: str = Field(..., min_length=1, description="Field name to extract")
    description: str = Field(..., min_length=1, description="Description of what to extract")

    @field_validator("field_name", "description")
    @classmethod
    def strip_string_values(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be empty or whitespace only.")
        return value


class ModelParameters(BaseModel):
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    top_k: int = Field(default=20, ge=1)


class ConfigurationCreateRequest(BaseModel):
    config_name: str = Field(..., min_length=1, description="User-friendly configuration name")
    document_type: str = Field(..., min_length=1, description="Document type, e.g. invoice")
    provider: str = Field(default=DEFAULT_PROVIDER, description="Provider name, e.g. gemini")
    model_name: str = Field(default=DEFAULT_MODEL_NAME, description="Model name to use")
    parameters: ModelParameters = Field(default_factory=ModelParameters)
    fields: list[FieldConfig] = Field(..., min_length=1, description="List of fields to extract")

    @field_validator("config_name", "document_type", "provider", "model_name")
    @classmethod
    def strip_main_string_values(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be empty or whitespace only.")
        return value

    @field_validator("provider")
    @classmethod
    def validate_provider(cls, value: str) -> str:
        normalized_value = value.lower().strip()
        if normalized_value not in SUPPORTED_PROVIDERS:
            raise ValueError(f"Unsupported provider: {value}")
        return normalized_value

    @field_validator("fields")
    @classmethod
    def validate_unique_field_names(cls, fields: list[FieldConfig]) -> list[FieldConfig]:
        field_names = [field.field_name.lower() for field in fields]
        if len(field_names) != len(set(field_names)):
            raise ValueError("Field names must be unique within one configuration.")
        return fields


class ConfigurationResponse(BaseModel):
    config_id: str
    config_name: str
    document_type: str
    provider: str
    model_name: str
    parameters: ModelParameters
    fields: list[FieldConfig]
    created_at: datetime
    updated_at: datetime