import fitz

def extrair_texto_pdf(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    texto_paginas = []

    for page in doc:
        texto_paginas.append(page.get_text())

    return "\n".join(texto_paginas)