import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field
from utility import DocOperation

doc_ops = DocOperation()
load_dotenv()

class Fields(BaseModel):
    BoundingBox : list[int] = Field(..., description="Get Bounding box of where the information found [y-min,x-min,y-max,x-max]")
    Page_No : int = Field(..., description="Get page number where there information found")

class NameField(Fields):
    value : str = Field(..., description="The recipient's Name found in the form body, Name is above the Address")

class AddressField(Fields):
    value : str = Field(..., description="The recipient's address found in the form body, NOT the sender's address in the header.")
    
class InvoiceModel(BaseModel):
    Name : NameField
    Address : AddressField
    

pdf_path = r'D:\aakash\SwitchFocus\Own_Project\DocuMind-Gen\Sample-Doc\7. Indra Engineering.pdf'

if not doc_ops.is_digital_native(pdf_path = pdf_path):
    client = genai.Client()

    prompt = """"
    Extract Name and Address with there BoundingBox and page number, For BoundingBox, provide [ymin, xmin, ymax, xmax], 
    where the top-left is [0,0] and bottom-right is [1000,1000]. 
    Ensure the box tightly surrounds the specific text value.
    Consider multiple page extraction from pdf.
    Extract and give each page name and address and provide page number and bounding box for each.
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