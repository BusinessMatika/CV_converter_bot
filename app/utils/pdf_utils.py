import fitz  # PyMuPDF


def extract_text_from_pdf(file_path: str) -> str:
    """Извлекает текст из PDF, обрабатывая таблицы и списки."""
    doc = fitz.open(file_path)
    extracted_text = []

    for page in doc:
        blocks = page.get_text("blocks")  # Получаем текстовые блоки с координатами
        blocks = sorted(blocks, key=lambda b: (b[1], b[0]))  # Сортируем по координатам

        page_text = []
        for block in blocks:
            text = block[4].strip()

            # Проверяем, выглядит ли текст как таблица (несколько пробелов / табуляций)
            if "\t" in text or "  " in text:
                text = text.replace("\t", " | ")  # Разделяем столбцы
                text = "TABLE: " + text  # Добавляем метку (можно убрать)

            # Проверяем, начинается ли строка с числа или маркера (список)
            elif text.startswith(("-", "*", "•", "▪", "‣")) or text[:2].isdigit():
                text = "LIST: " + text  # Добавляем метку списка (можно убрать)

            page_text.append(text)

        extracted_text.append("\n".join(page_text))

    return "\n\n".join(extracted_text)
