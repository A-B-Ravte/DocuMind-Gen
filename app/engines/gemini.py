from pathlib import Path

from google import genai

from app.core.settings import settings


class GeminiEngine:
    """
    Gemini-only provider engine for phase 2.
    """

    def __init__(self) -> None:
        settings.validate()
        self.client = genai.Client(api_key=settings.google_api_key)

    def extract_from_pdf(
        self,
        pdf_path: str | Path,
        prompt: str,
        model_name: str,
        parameters: dict,
    ) -> str:
        pdf_path = Path(pdf_path)
        file_data = pdf_path.read_bytes()

        response = self.client.models.generate_content(
            model=model_name,
            contents=[
                prompt,
                {
                    "inline_data": {
                        "data": file_data,
                        "mime_type": "application/pdf",
                    }
                },
            ],
            config={
                "temperature": parameters.get("temperature", 0.2),
                "top_p": parameters.get("top_p", 0.9),
                "top_k": parameters.get("top_k", 20),
                "response_mime_type": "application/json",
            },
        )

        return response.text