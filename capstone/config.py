from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

INPUT_FOLDER = os.getenv("INPUT_FOLDER", "data/pdfs")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "output")

CLASSIFICATION_MODEL = os.getenv(
    "CLASSIFICATION_MODEL",
    "gemini-2.5-flash"
)

EXTRACTION_MODEL = os.getenv(
    "EXTRACTION_MODEL",
    "gemini-2.5-flash"
)

OCR_MODEL = os.getenv(
    "OCR_MODEL",
    "gemini-2.5-flash"
)