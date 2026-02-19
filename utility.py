import fitz

class DocOperation():

    def is_digital_native(self, pdf_path):
        doc = fitz.open(pdf_path)
        for page in doc:
            # Check if page has text fonts
            if len(page.get_fonts()) > 0:
                return True # Has text, likely native
        return False # No fonts, likely scanned
    
    def get_annotated_doc(self, doc_details, document):
        doc = fitz.open(document)
        for key, mapping in doc_details.items():
            print("mapping is", mapping["BoundingBox"])
            #continue
            box = mapping["BoundingBox"]
            page_no = mapping["Page_No"]   

            if not box or box == [0,0,0,0]:
                continue

            
            if not box or box==[0,0,0,0]:
                return
            
            page = doc[page_no - 1]
            y, x, y1, x1 = box

            r = page.rect

            rect = fitz.Rect(
                (x/1000) * r.width,
                (y/1000) * r.height - 2,
                (x1/1000) * r.width,
                (y1/1000) * r.height
            )

            page.draw_rect(rect, color=(1,0,0), width=1)
            page.insert_text((rect.x0, rect.y0 - 5), key, color=(1, 0, 0), fontsize=8)

        doc.save('Anotated.pdf')
        doc.close()    
    

if __name__=="__main__":
    pdf_path = r'D:\aakash\SwitchFocus\Own_Project\DocuMind-Gen\Sample-Doc\Digital\1380821.pdf'
    ops = DocOperation()
    is_digital = ops.is_digital_native(pdf_path)

    
