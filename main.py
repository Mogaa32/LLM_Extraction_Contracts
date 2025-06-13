import setup  # Loads environment variables
from setup import PDF_PATH
from data_extraction import extract_structured_data_from_pdf
from gemini_api import extract_structured_data
from data_structure import add_entry, location_data
import pprint
import time

MAX_LEN = 20000
failed_chunks = []

if __name__ == "__main__":
    pdf_path = PDF_PATH

    print("📄 Extracting content from PDF...")
    data = extract_structured_data_from_pdf(pdf_path)
    current_state = None

    print(f"🔍 Processing {len(data['tables'])} tables and {len(data['other_chunks'])} text chunks...\n")

    for i, chunk in enumerate(data["tables"] + data["other_chunks"]):
        text = chunk["content"] if isinstance(chunk, dict) and "content" in chunk else chunk
        chunk_type = "table" if i < len(data["tables"]) else "text"
        chunk_index = i + 1

        if len(text) > MAX_LEN:
            print(f"⚠️ Skipping long {chunk_type} {chunk_index} (> {MAX_LEN} chars)")
            failed_chunks.append({
                "index": chunk_index,
                "type": chunk_type,
                "reason": "Too long",
                "preview": text[:300]
            })
            continue

        try:
            result = extract_structured_data(text, current_state)
            current_state = result.get("current_state", current_state)
            for entry in result["entries"]:
                add_entry(entry)
        except Exception as e:
            print(f"⚠️ Error processing {chunk_type} {chunk_index}: {e}")
            failed_chunks.append({
                "index": chunk_index,
                "type": chunk_type,
                "error": str(e),
                "preview": text[:300]
            })
        time.sleep(2)

    print("\n✅ Final structured location data:")
    pprint.pprint(location_data)

    if failed_chunks:
        print("\n❌ Failed Chunks:")
        pprint.pprint(failed_chunks)
