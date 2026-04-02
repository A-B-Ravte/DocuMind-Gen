class PromptManager:
    """
    Builds extraction prompts from saved configuration.
    """

    @staticmethod
    def build_extraction_prompt(config_data: dict) -> str:
        field_lines = []

        for field in config_data.get("fields", []):
            field_name = field["field_name"]
            description = field["description"]
            field_lines.append(f"- {field_name}: {description}")

        joined_fields = "\n".join(field_lines)

        prompt = f"""
You are given a document. Extract the requested fields and return a strict JSON object.

For every requested field, return:
- value
- BoundingBox
- Page_No

BoundingBox rules:
- Provide BoundingBox as [ymin, xmin, ymax, xmax]
- Coordinates must be normalized from 0 to 1000
- Top-left is [0,0]
- Bottom-right is [1000,1000]
- Bounding box must tightly wrap only the extracted value text

Page_No rules:
- Page number must start from 1

Requested fields:
{joined_fields}

Output rules:
- Return valid JSON only
- Use the exact field names provided
- If a value is not found, still return the field with:
  - value as empty string
  - BoundingBox as [0, 0, 0, 0]
  - Page_No as 0
"""
        return prompt.strip()