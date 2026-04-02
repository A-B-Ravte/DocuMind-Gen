from pathlib import Path

import fitz

from app.core.constants import ANNOTATED_PDF_FILENAME


class AnnotationService:
    """
    Handles annotated PDF generation using extracted result JSON.
    """

    @staticmethod
    def create_annotated_pdf(
        input_pdf_path: str | Path,
        extracted_data: dict,
        output_dir: str | Path,
    ) -> Path:
        input_pdf_path = Path(input_pdf_path)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        annotated_pdf_path = output_dir / ANNOTATED_PDF_FILENAME

        doc = fitz.open(input_pdf_path)

        for field_name, field_value in extracted_data.items():
            box = field_value.get("BoundingBox", [0, 0, 0, 0])
            page_no = field_value.get("Page_No", 0)

            if not box or box == [0, 0, 0, 0] or page_no <= 0:
                continue

            page = doc[page_no - 1]
            ymin, xmin, ymax, xmax = box

            page_rect = page.rect

            rect = fitz.Rect(
                (xmin / 1000) * page_rect.width,
                (ymin / 1000) * page_rect.height - 3,
                (xmax / 1000) * page_rect.width,
                (ymax / 1000) * page_rect.height,
            )

            page.draw_rect(rect, color=(1, 0, 0), width=1)
            page.insert_text(
                (rect.x0, rect.y0 - 5),
                field_name,
                color=(1, 0, 0),
                fontsize=8,
            )

        doc.save(annotated_pdf_path)
        doc.close()

        return annotated_pdf_path