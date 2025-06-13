# 📄 LLM Extraction Pipeline

This project extracts structured data from carrier contract PDFs using OCR and the Gemini API. The flow includes reading PDF files, extracting tables and text, processing them with LLM prompts, and organizing the results in a nested data structure.

## 🧱 Project Structure
```
LLM_Extraction/
├── main.py              # Main pipeline entry point
├── setup.py             # Loads environment variables & config (PDF path, API keys)
├── data_extraction.py   # Extracts text and tables from PDF using Unstructured + OCR
├── gemini_api.py        # Formats prompt and calls Gemini API
├── data_structure.py    # Adds entries to the nested location structure
├── try_fix.py           # Utility to clean and fix malformed JSON responses
├── .env                 # Environment variables (NOT tracked by Git)
└──  .gitignore           # Ignore .env, __pycache__, etc.

-Flow_chart.text      # Has the working and flow of the code for each file
-requirements.txt     # Lists all Python dependencies
-README.md            # Project overview and usage guide
```

## 🚀 How to Run

1. Clone the repo and set up a virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate   # For Windows
    pip install -r requirements.txt
    ```

2. Create a `.env` file with:
    ```env
    GEMINI_API_KEY=your-api-key-here
    TESSERACT_PATH=full/path/to/tesseract.exe
    PDF_PATH=full/path/to/your_pdf.pdf
    ```

3. Run the pipeline:
    ```bash
    python main.py
    ```

## 📦 Requirements

- Python 3.8+
- Tesseract OCR installed
- Google Gemini API key

## 🧠 What it does

- Segments PDF into text and tables
- Sends chunks to Gemini API
- Structures results into `location_data`
- Handles malformed JSON responses

## 📂 Output

Prints structured nested dictionary of locations and extracted info.

---
