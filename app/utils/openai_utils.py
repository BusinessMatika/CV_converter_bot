import io
import json

import openai
from docx import Document
from telegram import Update
from telegram.ext import ContextTypes

from app.common.enums import EditCV, EvaluateVacancyCV, OpenAI
from app.config import OPENAI_API_KEY, logger

from .docx_utils import generate_docx_from_json

openai.api_key = OPENAI_API_KEY


async def analyze_and_edit_cv(
        update: Update, context: ContextTypes.DEFAULT_TYPE,
        template_choice: str, language_choice: str,
        user_text: str
) -> io.BytesIO:
    """Analyze and edit CV text taking into account styles."""

    if not user_text:
        logger.error("File is empty.")
        return "Error: No readable content found."

    if language_choice == 'russian':
        json_choice = EditCV.JSON_RUS.value
        prompt_choice = language_choice
    elif language_choice == 'english':
        json_choice = EditCV.JSON_ENG.value
        prompt_choice = language_choice
    else:
        logger.error("Ошибка: неверный выбор языка")
        return "Invalid language choice"

    try:
        response = openai.chat.completions.create(
            model=OpenAI.MODEL_3_5_TURBO.value,
            messages=EditCV.get_messages(
                user_content=user_text,
                json_str=json_choice,
                prompt_choice=prompt_choice
            ),
            temperature=0
        )
        gpt_response = response.choices[0].message.content
    except Exception as e:
        logger.error(f'Ошибка запроса к OpenAI: {e}')
        return 'OpenAI request failed'

    try:
        gpt_response_clean = gpt_response.strip()
        gpt_response_clean = gpt_response.replace("\n", "").replace("'", '"')
        gpt_json = json.loads(gpt_response_clean)
    except json.JSONDecodeError as e:
        try:
            gpt_json = json.loads(gpt_response)
        except:
            return 'Response error from OpenAI'

    if "sections" not in gpt_json:
        logger.error("Ошибка: JSON-ответ не содержит ключ 'sections'.")
        return "Error: Missing 'sections' in response."

    output_stream = io.BytesIO()
    generate_docx_from_json(gpt_json, output_stream, template_choice, language_choice)
    output_stream.seek(0)
    return output_stream


async def analyze_vacancy(
        update: Update, context: ContextTypes.DEFAULT_TYPE,
        user_text: str):
    if not user_text:
        logger.error("Vacancy is empty.")
        return "Error: No readable content found."
    
    try:
        response = openai.chat.completions.create(
            model=OpenAI.MODEL_3_5_TURBO.value,
            messages=EvaluateVacancyCV.get_messages(
                vacancy_data=user_text,
                prompt_choice=EvaluateVacancyCV.eval_vac_prompt.value
            ),
            temperature=0
        )
        gpt_response = response.choices[0].message.content
    except Exception as e:
        logger.error(f'Ошибка запроса к OpenAI: {e}')
        return 'OpenAI request failed'

    try:
        gpt_response_clean = gpt_response.strip().replace("\n", "").replace("'", '"')
        gpt_json = json.loads(gpt_response_clean)
        logger.info(f"GPT_JSON СОДЕРЖИТ {json.dumps(gpt_json, ensure_ascii=False)}")
    except json.JSONDecodeError as e:
        try:
            gpt_json = json.loads(gpt_response)
            logger.debug(f'GPT_JSON СОДЕРЖИТ {gpt_json}')
        except:
            return 'Response error from OpenAI'

    return gpt_json


async def analyze_vacancy_and_cv(
        update: Update, context: ContextTypes.DEFAULT_TYPE,
        cv_data: str, vacancy_data: str
):
    if not cv_data:
        logger.error("CV is empty.")
        return "Error: No readable content found."
    logger.info(f'ПОКАЗАТЬ ЧТО СОДЕРЖИТСЯ В VACANCY_DATA: {vacancy_data}, А ТАКЖЕ КАКОЙ ЭТО ТИП ДАННЫХ: {type(vacancy_data)}')
    try:
        response = openai.chat.completions.create(
            model=OpenAI.MODEL_4_TURBO.value,
            messages=EvaluateVacancyCV.get_messages(
                vacancy_data=vacancy_data,
                cv_data=cv_data,
                prompt_choice=EvaluateVacancyCV.eval_vac_cv_prompt.value
            ),
            temperature=0
        )
        gpt_response = response.choices[0].message.content
    except openai.OpenAIError as e:
        logger.error(f'Ошибка OpenAI API: {e}')
        return f'OpenAI API error: {e}'

    except ValueError as e:
        logger.error(f'Ошибка обработки ответа: {e}')
        return f'Response processing error: {e}'

    except Exception as e:
        logger.error(f'Неизвестная ошибка: {e}', exc_info=True)
        return f'Unknown error: {e}'

    gpt_response_clean = gpt_response.strip()

    logger.debug(f'GPT_JSON СОДЕРЖИТ {gpt_response_clean}')

    return gpt_response_clean
