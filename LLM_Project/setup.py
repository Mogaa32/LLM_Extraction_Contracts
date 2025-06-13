import os
import pytesseract
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_PATH")
os.environ["OCR_AGENT"] = "unstructured_pytesseract.pytesseract.PyTesseractAgent"
PDF_PATH = os.getenv("PDF_PATH")