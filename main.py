import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field
from utility import DocOperation

doc_ops = DocOperation()
load_dotenv()

class Fields(BaseModel):
    BoundingBox : list[int] = Field(..., description="Get Bounding box of where the information found.")
    Page_No : int = Field(..., description="Get page number where there information found")

class NameField(Fields):
    value : str = Field(..., description="Search for Name provided at the start of document.")

class AddressField(Fields):
    value : str = Field(..., description="Address provided at the start below the Name.")
    
class InvoiceModel(BaseModel):
    Name : NameField
    Address : AddressField
    

pdf_path = r'D:\aakash\SwitchFocus\Own_Project\DocuMind-Gen\Sample-Doc\7. Indra Engineering.pdf'

if not doc_ops.is_digital_native(pdf_path = pdf_path):
    client = genai.Client()

    prompt = """"
    Extract the multi page document and get the Name and Address fields, 
    Document provided can have single page or multiple page both in jpg, jpeg, png or pdf formats
    Return json properly that matches the Provided Schema.
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
    doc_details = doc.model_dump()
else :
    pass # if pdf is digital then save cost of api and go by traditional way.

doc_ops.get_annotated_doc(doc_details, pdf_path)