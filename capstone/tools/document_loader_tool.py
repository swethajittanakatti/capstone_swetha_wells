from pypdf import PdfReader

from tools.ocr_tool import ocr_pdf


def load_document(file_path: str):

    text = ""

    try:

        reader = PdfReader(file_path)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

    except Exception:
        pass

    if len(text.strip()) < 100:

        print(f"OCR triggered for {file_path}")

        text = ocr_pdf(file_path)

    return text