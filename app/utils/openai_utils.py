import io
import json
import os

import openai
from docx import Document

from app.common.enums import OpenAI
from app.config import OPENAI_API_KEY, logger

from .docx_utils import generate_docx_from_json

openai.api_key = OPENAI_API_KEY


def _extract_table_text(table):
    # Extract text from a table using python-docx's Document
    table_text = []
    for row in table.rows:
        row_text = [cell.text.strip() for cell in row.cells]
        table_text.append(row_text)
    return table_text


async def analyze_and_edit(user_text: str, template_choice: str, language_choice: str) -> io.BytesIO:
    """Analyzes and edits raw text content and tables."""

    # Проверка существования файла перед открытием
    if user_text.endswith('.docx'):
        if not os.path.exists(user_text):
            logger.error(f"Файл {user_text} не найден.")
            return "Error: File not found."

        user_doc = Document(user_text)
        full_text = []

        # Read elements one-by-one (paragraphs and tables)
        for element in user_doc.element.body:
            if element.tag.endswith("p"):  # paragraph
                text = element.text.strip()
                if text:
                    full_text.append(text)
            elif element.tag.endswith("tbl"):  # table
                # Convert the CT_Tbl element into a Table object
                table = user_doc.tables[len(full_text) // 2]  # Grab the corresponding Table object
                table_text = _extract_table_text(table)

                # Convert each row of the table into a string and join them
                table_text_str = "\n".join(["\t".join(row) for row in table_text])
                full_text.append(table_text_str)

        user_text = "\n".join(full_text).strip()

    if language_choice == 'russian':
        json_choice = OpenAI.JSON_RUS.value
        prompt_choice = language_choice
        logger.info(f'JSON and PROMPT chosen for russian language.')
    elif language_choice == 'english':
        json_choice = OpenAI.JSON_ENG.value
        prompt_choice = language_choice
        logger.info(f'JSON and PROMPT chosen for english language.')
    else:
        logger.error("Ошибка: неверный выбор языка")
        return "Invalid language choice"

    # Get response from OpenAI
    try:
        response = openai.chat.completions.create(
            model=OpenAI.MODEL.value,
            messages=OpenAI.get_messages(
                user_content=user_text,
                json_str=json_choice,
                prompt_choice=prompt_choice
            ),
            temperature=0, top_p=0.1
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

    # Проверка наличия ключевых секций в JSON
    if "sections" not in gpt_json:
        logger.error("Ошибка: JSON-ответ не содержит ключ 'sections'.")
        return "Error: Missing 'sections' in response."

    for section in json_choice["sections"]:
        if section not in gpt_json["sections"] or not gpt_json["sections"][section].get("title"):
            logger.error(f"Ошибка: секция {section} не заполнена корректно")
            return f"Error: section {section} is not filled correctly."

    # Create docx from JSON
    output_stream = io.BytesIO()
    generate_docx_from_json(gpt_json, output_stream, template_choice, language_choice)
    output_stream.seek(0)
    return output_stream
