from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import Table


def extract_structured_data_from_pdf(pdf_path):
    elements = partition_pdf(filename=pdf_path, strategy="hi_res", languages=["eng"])
    tables = []
    chunks = []
    temp = ""
    limit = 1500
    for el in elements:
        if isinstance(el, Table):
            if hasattr(el, 'text_as_html') and el.text_as_html:
                tables.append({"type": "table_html", "content": el.text_as_html})
            elif hasattr(el, 'text_as_markdown') and el.text_as_markdown:
                tables.append({"type": "table_markdown", "content": el.text_as_markdown})
            else:
                tables.append({"type": "table_text", "content": el.text.strip()})
            if temp:
                chunks.append(temp.strip())
                temp = ""
        else:
            text = el.text.strip()
            if text:
                temp += text + "\n"
                if len(temp) > limit:
                    chunks.append(temp.strip())
                    temp = ""
    if temp:
        chunks.append(temp.strip())
    return {"tables": tables, "other_chunks": chunks}
