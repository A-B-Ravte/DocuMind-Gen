import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

load_dotenv()

class InvoiceModel(BaseModel):
    Name : str = Field(..., description="Name provided at the start of document.")
    Address : str = Field(..., description="Address provided at the start below the Name.")

client = genai.Client()

prompt = """"
Extract the document and get the Name and Address fields 
Return only JSON that matches the Provided Schema.
"""

document = client.files.upload(file = r'Sample-Doc\Alfa_1.jpg')
response = client.models.generate_content(
    model = 'gemini-2.5-flash',
    contents = [document, prompt],
    config={
        'response_mime_type' : 'application/json',
        'response_schema' : InvoiceModel
    }

)

doc = InvoiceModel.model_validate_json(response.text)
print(doc.model_dump())