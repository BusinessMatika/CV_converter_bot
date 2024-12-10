import openai
from docx import Document

from common.enums import OpenAI
from config import EDITED_CV, REFERENCE_CV


async def analyze_and_edit(
        user_file_path: str,
        reference_file_path: str = REFERENCE_CV
) -> str:

    # Load user's file
    user_doc = Document(user_file_path)
    user_content = '\n'.join([p.text for p in user_doc.paragraphs])

    # Load reference file
    reference_doc = Document(REFERENCE_CV)
    reference_content = '\n'.join([p.text for p in reference_doc.paragraphs])

    response = openai.chat.completions.create(
        model=OpenAI.MODEL.value,
        messages=OpenAI.get_messages(
            user_content=user_content,
            reference_content=reference_content
        )
    )

    gpt_response = response.choices[0].message.content

    # Check if edits are needed (CHECK WHETHER THIS CONDITION IS NEEDED!)
    if 'The document is compatible' in gpt_response:
        return None

    edited_file_path = EDITED_CV
    edited_doc = Document()
    for line in gpt_response.split('\n'):
        edited_doc.add_paragraph(line)
    edited_doc.save(edited_file_path)

    return edited_file_path
