from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.paths import TEMPLATES_DIR
from app.managers.config_manager import ConfigManager
from app.schemas.config_schema import (
    ConfigurationCreateRequest,
    ConfigurationResponse,
    FieldConfig,
    ModelParameters,
)

router = APIRouter(prefix="/config", tags=["Configuration"])
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

config_manager = ConfigManager()


@router.get("/", response_class=HTMLResponse)
def config_page(request: Request):
    configurations = config_manager.list_configurations()

    return templates.TemplateResponse(
        "config.html",
        {
            "request": request,
            "configurations": configurations,
            "page_title": "Configuration Management",
        },
    )


@router.post("/create", response_model=ConfigurationResponse)
def create_configuration(
    config_name: str = Form(...),
    document_type: str = Form(...),
    provider: str = Form(...),
    model_name: str = Form(...),
    temperature: float = Form(...),
    top_p: float = Form(...),
    top_k: int = Form(...),
    field_names: list[str] = Form(...),
    field_descriptions: list[str] = Form(...),
):
    if len(field_names) != len(field_descriptions):
        raise HTTPException(
            status_code=400,
            detail="Each field name must have a matching field description.",
        )

    fields: list[FieldConfig] = []
    for field_name, field_description in zip(field_names, field_descriptions):
        if field_name.strip() and field_description.strip():
            fields.append(
                FieldConfig(
                    field_name=field_name.strip(),
                    description=field_description.strip(),
                )
            )

    if not fields:
        raise HTTPException(
            status_code=400,
            detail="At least one valid field is required.",
        )

    config_request = ConfigurationCreateRequest(
        config_name=config_name.strip(),
        document_type=document_type.strip(),
        provider=provider.strip(),
        model_name=model_name.strip(),
        parameters=ModelParameters(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
        ),
        fields=fields,
    )

    return config_manager.create_configuration(config_request)


@router.get("/all", response_model=list[ConfigurationResponse])
def list_all_configurations():
    return config_manager.list_configurations()


@router.get("/{config_id}", response_model=ConfigurationResponse)
def get_configuration(config_id: str):
    try:
        return config_manager.get_configuration(config_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc