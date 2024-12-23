import io
import json

import openai
from docx import Document

from common.enums import OpenAI

from .docx_utils import generate_docx_from_json


async def analyze_and_edit(
        user_file_path: str,
) -> io.BytesIO:
    """Analyzes and edits user's document."""
    # Load user's file
    user_doc = Document(user_file_path)
    user_content = '\n'.join(
        [p.text for p in user_doc.paragraphs if p.text.strip()]
    ).strip()

    # Get response from OpenAI
    response = openai.chat.completions.create(
        model=OpenAI.MODEL.value,
        messages=OpenAI.get_messages(
            user_content=user_content,
            json_str=OpenAI.JSON.value,
        )
    )

    gpt_response = response.choices[0].message.content

    # Parse JSON response
    try:
        gpt_json = json.loads(gpt_response)
    except json.JSONDecodeError as e:
        print("Ошибка в JSON:", e)
        return "Ошибка в формате ответа от OpenAI"

    # Validate required sections
    for section in OpenAI.JSON.value["sections"]:
        if not gpt_json["sections"].get(section, {}).get("title"):
            print(f"Ошибка: секция {section} не заполнена корректно.")
            return f"Ошибка: секция {section} не заполнена корректно."

    # Generate DOCX from JSON
    output_stream = io.BytesIO()
    generate_docx_from_json(gpt_json, output_stream)
    output_stream.seek(0)
    return output_stream
