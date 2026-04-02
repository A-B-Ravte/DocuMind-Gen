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

            page = doc[page_no - 1]
            ymin, xmin, ymax, xmax = box

            r = page.rect

            rect = fitz.Rect(
                (xmin/1000) * r.width,
                (ymin/1000) * r.height - 3,
                (xmax/1000) * r.width,
                (ymax/1000) * r.height
            )

            page.draw_rect(rect, color=(1,0,0), width=1)
            page.insert_text((rect.x0, rect.y0 - 5), key, color=(1, 0, 0), fontsize=8)

        doc.save('Anotated.pdf')
        doc.close()    
    

if __name__=="__main__":
    pdf_path = r'D:\aakash\SwitchFocus\Own_Project\DocuMind-Gen\Sample-Doc\Digital\1380821.pdf'
    ops = DocOperation()
    is_digital = ops.is_digital_native(pdf_path)

    
