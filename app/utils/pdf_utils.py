def extract_text_from_pdf(file_path: str) -> str:
    import fitz
    """Извлекает текст из PDF, обрабатывая таблицы и списки."""
    doc = fitz.open(file_path)
    extracted_text = []

    for page in doc:
        blocks = page.get_text("blocks")
        blocks = sorted(blocks, key=lambda b: (b[1], b[0]))

        page_text = []
        for block in blocks:
            text = block[4].strip()

            if "\t" in text or "  " in text:
                text = text.replace("\t", " | ")
                text = "TABLE: " + text

            elif text.startswith(("-", "*", "•", "▪", "‣")) or text[:2].isdigit():
                text = "LIST: " + text

            page_text.append(text)

        extracted_text.append("\n".join(page_text))

    return "\n\n".join(extracted_text)
