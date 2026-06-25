import time
from google import genai
from google.genai.errors import ServerError

from config import GOOGLE_API_KEY, OCR_MODEL

client = genai.Client(
    api_key=GOOGLE_API_KEY
)


def ocr_pdf(pdf_path):

    for attempt in range(5):

        try:

            uploaded_file = client.files.upload(
                file=pdf_path
            )
            print(f"Starting OCR for {pdf_path}")
            response = client.models.generate_content(
                model=OCR_MODEL,
                contents=[
                    uploaded_file,
                    "Extract all text from this PDF."
                ]
            )
            print("OCR completed")
            return response.text

        except ServerError:

            wait_time = 15 * (attempt + 1)

            print(
                f"Gemini busy. Waiting {wait_time}s..."
            )

            time.sleep(wait_time)

    raise Exception(
        "OCR failed after retries."
    )