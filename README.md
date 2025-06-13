# 📄 LLM Extraction Pipeline

This project extracts structured data from carrier contract PDFs using OCR and the Gemini API. The flow includes reading PDF files, extracting tables and text, processing them with LLM prompts, and organizing the results in a nested data structure.

## 🧱 Project Structure

LLM_Extraction/
│
├── main.py # Main pipeline entry
├── setup.py # Loads environment variables & config
├── data_extraction.py # PDF partitioning and OCR using Unstructured
├── gemini_api.py # Gemini API call and prompt formatting
├── data_structure.py # Adds entries to the nested structure
├── try_fix.py # Utility to fix malformed JSON from LLM
├── .env # API keys and config (not tracked by Git)
├── .gitignore # Ignore config and cache files
├── requirements.txt # Python dependencies
├── README.md # This file


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
