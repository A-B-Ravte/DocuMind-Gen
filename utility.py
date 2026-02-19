import fitz

class DocOperation():

    def is_digital_native(self, pdf_path):
        doc = fitz.open(pdf_path)
        for page in doc:
            # Check if page has text fonts
            if len(page.get_fonts()) > 0:
                return True # Has text, likely native
        return False # No fonts, likely scanned

if __name__=="__main__":
    pdf_path = r'D:\aakash\SwitchFocus\Own_Project\DocuMind-Gen\Sample-Doc\Digital\1380821.pdf'
    ops = DocOperation()
    is_digital = ops.is_digital_native(pdf_path)

    print(is_digital)
