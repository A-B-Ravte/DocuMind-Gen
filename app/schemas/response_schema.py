from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str
    details: str | None = None