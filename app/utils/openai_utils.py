import io
import json
import os
from typing import Optional

import openai
from docx import Document
from telegram import Update
from telegram.ext import ContextTypes

from app.common.enums import OpenAI
from app.config import OPENAI_API_KEY, logger

from .docx_utils import generate_docx_from_json

openai.api_key = OPENAI_API_KEY


def _extract_table_text(table):
    """Retrieve text from table."""
    table_text = []
    for row in table.rows:
        row_text = [cell.text.strip() if cell.text.strip() else "-" for cell in row.cells]  # "-" для пустых ячеек
        if any(cell != "-" for cell in row_text):  # Добавляем только строки с данными
            table_text.append("\t".join(row_text))  # Объединяем ячейки через табуляцию
    return "\n".join(table_text).strip()  # Возвращаем строку с переносами строк между рядами


def extract_text_from_docx(doc_path):
    """
    DOCX parser: retrieve text, lists, tables.
    """
    if not os.path.exists(doc_path):
        logger.error(f"File {doc_path} not found.")
        return "Error: File not found."

    doc = Document(doc_path)
    extracted_text = []

    # Обработка параграфов
    for para in doc.paragraphs:
        if para.text.strip():  # Проверка, что текст не пустой
            extracted_text.append(para.text)

    # Обработка таблиц
    for table in doc.tables:
        table_text = _extract_table_text(table)
        if table_text.strip():  # Проверка на пустоту таблицы
            extracted_text.append(table_text)

    if not extracted_text:
        logger.error("File is empty.")
        return "Error: No readable content found."

    return "\n".join(extracted_text).strip()  # Объединяем все текстовые данные в одну строку


async def analyze_and_edit(
        update: Update, context: ContextTypes.DEFAULT_TYPE,
        template_choice: str, language_choice: str,
        user_file: Optional[str] = None, user_text: Optional[str] = None
) -> io.BytesIO:
    """Analyze and edit CV text taking into account styles."""

    if user_file:
        text = extract_text_from_docx(user_file)
    else:
        text = user_text

    if not text:
        logger.error("File is empty.")
        return "Error: No readable content found."

    # JSON-template choose based on language choice
    if language_choice == 'russian':
        json_choice = OpenAI.JSON_RUS.value
        prompt_choice = language_choice
    elif language_choice == 'english':
        json_choice = OpenAI.JSON_ENG.value
        prompt_choice = language_choice
    else:
        logger.error("Ошибка: неверный выбор языка")
        return "Invalid language choice"

    # Get response from OpenAI
    try:
        response = openai.chat.completions.create(
            model=OpenAI.MODEL.value,
            messages=OpenAI.get_messages(
                user_content=text,
                json_str=json_choice,
                prompt_choice=prompt_choice
            ),
            temperature=0
        )
        gpt_response = response.choices[0].message.content
    except Exception as e:
        logger.error(f'Ошибка запроса к OpenAI: {e}')
        return 'OpenAI request failed'

    # Parse JSON
    try:
        gpt_response_clean = gpt_response.strip()
        gpt_response_clean = gpt_response.replace("\n", "").replace("'", '"')
        gpt_json = json.loads(gpt_response_clean)
        logger.debug(f'GPT_JSON СОДЕРЖИТ {gpt_json}')
    except json.JSONDecodeError as e:
        try:
            gpt_json = json.loads(gpt_response)
            logger.debug(f'GPT_JSON СОДЕРЖИТ {gpt_json}')
        except:
            return 'Response error from OpenAI'

    if "sections" not in gpt_json:
        logger.error("Ошибка: JSON-ответ не содержит ключ 'sections'.")
        return "Error: Missing 'sections' in response."

    # Create docx from JSON
    output_stream = io.BytesIO()
    generate_docx_from_json(gpt_json, output_stream, template_choice, language_choice)
    output_stream.seek(0)
    return output_stream
