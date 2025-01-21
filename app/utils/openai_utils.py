import io
import json

import openai
from docx import Document

from app.common.enums import OpenAI
from app.config import OPENAI_API_KEY

from .docx_utils import generate_docx_from_json

openai.api_key = OPENAI_API_KEY


async def analyze_and_edit(user_text: str, format_choice: str) -> io.BytesIO:
    """Analyzes and edits raw text content."""
    if '.docx' in user_text:
        user_doc = Document(user_text)
        user_text = '\n'.join(
            [p.text for p in user_doc.paragraphs if p.text.strip()]
        ).strip()

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

    # Parse JSON response
    try:
        gpt_json = json.loads(gpt_response)
    except json.JSONDecodeError as e:
        return "Ошибка в формате ответа от OpenAI"

    # Validate required sections
    for section in OpenAI.JSON.value["sections"]:
        if not gpt_json["sections"].get(section, {}).get("title"):
            return f"Ошибка: секция {section} не заполнена корректно."

    # Generate DOCX from JSON
    output_stream = io.BytesIO()
    generate_docx_from_json(gpt_json, output_stream, format_choice)
    output_stream.seek(0)
    return output_stream
