import io
import json

import openai
from docx import Document
from lxml import etree

from app.common.enums import OpenAI
from app.config import OPENAI_API_KEY, logger

from .docx_utils import generate_docx_from_json

openai.api_key = OPENAI_API_KEY


async def analyze_and_edit(user_text: str, template_choice: str) -> io.BytesIO:
    """Analyzes and edits raw text content and tables."""

    if user_text.endswith('.docx'):
        user_doc = Document(user_text)
        full_text = []

        # Read elements one-by-one (paragraphs and tables)
        for element in user_doc.element.body:
            if element.tag.endswith("p"):  # paragraph
                text = element.text.strip()
                if text:
                    full_text.append(text)

            elif element.tag.endswith("tbl"):  # table
                table = _extract_table_text(element)
                full_text.append(table)

        user_text = "\n".join(full_text).strip()

    if not template_choice:
        logger.error("template_choice is None or empty in analyze_and_edit!")

    # Get response from OpenAI
    response = openai.chat.completions.create(
        model=OpenAI.MODEL.value,
        messages=OpenAI.get_messages(
            user_content=user_text,
            json_str=OpenAI.JSON.value,
        ),
        temperature=0
    )

    gpt_response = response.choices[0].message.content

    # Parse JSON
    try:
        gpt_json = json.loads(gpt_response)
    except json.JSONDecodeError:
        logger.error("Ошибка разбора JSON-ответа от OpenAI")
        return "Response error from OpenAI"

    for section in OpenAI.JSON.value["sections"]:
        if not gpt_json["sections"].get(section, {}).get("title"):
            logger.error(f"Ошибка: секция {section} не заполнена корректно")
            return f"Error: section {section} is not filled correctly."

    # Create docx from JSON
    output_stream = io.BytesIO()
    generate_docx_from_json(gpt_json, output_stream, template_choice)
    output_stream.seek(0)
    return output_stream


def _extract_table_text(table_element) -> str:
    """Retrieve text from docx table."""
    table_text = ["TABLE:"]
    table = etree.ElementTree(table_element)

    for row in table.findall(".//w:tr", namespaces={"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}):
        cells = row.findall(".//w:tc", namespaces={"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"})
        row_text = " | ".join(" ".join(cell.itertext()).strip() for cell in cells)
        if row_text:
            table_text.append(row_text)

    return "\n".join(table_text)

