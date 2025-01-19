import pdfplumber


def extract_text_from_pdf(file_path: str) -> str:
    """Extracts all text from a PDF file."""
    full_text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)
    return "\n".join(full_text)
