import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field
from utility import DocOperation

doc_ops = DocOperation()
load_dotenv()

class InvoiceModel(BaseModel):
    Name : str = Field(..., description="Name provided at the start of document.")
    Address : str = Field(..., description="Address provided at the start below the Name.")
    BoundingBox : list[int] = Field(..., description="Bounding box of where the information found.")
    Page_No : int = Field(..., description="page number where there information found")

pdf_path = r'D:\aakash\SwitchFocus\Own_Project\DocuMind-Gen\Sample-Doc\Alfa_1.jpg'

if not doc_ops.is_digital_native(pdf_path = pdf_path):
    client = genai.Client()

    prompt = """"
    Extract the multi page document and get the Name and Address fields, 
    Document provided can have single page or multi page both in jpg, jpeg, png or pdf formats
    Return list of json data per page vise that matches the Provided Schema.
    Give me the bonding ractangles
    """

    document = client.files.upload(file = pdf_path)
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
else :
    pass # if pdf is digital then save cost of api and go by traditional way.

