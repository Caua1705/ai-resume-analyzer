import fitz


def extract_pdf_text(pdf_bytes: bytes) -> str:

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    pages_text = []

    for page in doc:
        pages_text.append(page.get_text())

    return "\n".join(pages_text)