import fitz

class DocOperation():

    def is_digital_native(self, pdf_path):
        doc = fitz.open(pdf_path)
        for page in doc:
            # Check if page has text fonts
            if len(page.get_fonts()) > 0:
                return True # Has text, likely native
        return False # No fonts, likely scanned
    
    def get_annotated_doc(self, page_no, box, document):
        doc = fitz.open(document)
        if not box or box==[0,0,0,0]:
            return
        
        page = doc[page_no - 1]
        x, y, x1, y1 = box

        r = page.rect

        rect = fitz.Rect(
            (x/1000) * r.width,
            (y/1000) * r.height,
            (x1/1000) * r.width,
            (y1/1000) * r.height
        )

        page.draw_rect(rect, color=(1,0,0), width=2)
    

if __name__=="__main__":
    pdf_path = r'D:\aakash\SwitchFocus\Own_Project\DocuMind-Gen\Sample-Doc\Digital\1380821.pdf'
    ops = DocOperation()
    is_digital = ops.is_digital_native(pdf_path)

    
