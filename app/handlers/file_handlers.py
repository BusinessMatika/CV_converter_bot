import os

from telegram import Update
from telegram.ext import ContextTypes

from app.common.constants import (ALLOWED_LANGUAGES, DOCX_MIME_TYPE,
                                  PDF_MIME_TYPE)
from app.common.enums import Reply
from app.config import DEBUG, logger
from app.utils.bot_utils import (get_user_language_choice,
                                 get_user_template_choice,
                                 send_message_or_edit_text)
from app.utils.openai_utils import analyze_and_edit
from app.utils.pdf_utils import extract_text_from_pdf


async def handle_file(
        update: Update, context: ContextTypes.DEFAULT_TYPE,
        template=None, language=None):
    """
    Handles the file received from the user, processes it,
    and sends back the edited document.
    """
    user_id = str(update.message.from_user.id)
    document = update.message.document
    user_file_name = document.file_name
    logger.info(f"Received file: {user_file_name}")
    if DEBUG:
        template_choice = context.user_data.get('cv_template')
        language_choice = context.user_data.get('chosen_language')
        logger.info(
            f'CV will be edited in accordance with template: {template_choice}. '
            f'CV language will be {language_choice}.'
        )
        file_path = f'{user_file_name}'
    else:
        template_choice = get_user_template_choice(user_id)
        language_choice = get_user_language_choice(user_id)
        logger.info(
            f'CV will be edited in accordance with template: {template_choice}. '
            f'CV language will be {language_choice}.'
        )
        file_path = os.path.join('/tmp', user_file_name)

    file = await context.bot.get_file(document.file_id)
    await file.download_to_drive(file_path)
    logger.info(f'CV saved to {file_path}')

    if language_choice:
        await send_message_or_edit_text(
            update,
            context,
            Reply.EDIT_CV_EXECUTION.value.format(
                file_name=user_file_name,
                template_name=template_choice.capitalize(),
                language_name=ALLOWED_LANGUAGES.get(language_choice)
            ),
            parse_mode='HTML')

    if document.mime_type == DOCX_MIME_TYPE:
        edited_file_stream = await analyze_and_edit(file_path, template_choice, language_choice)
        new_file_name = f"edited_{user_file_name}"
        logger.info(f"DOCX file edited: {new_file_name}")
    elif document.mime_type == PDF_MIME_TYPE:
        pdf_text = extract_text_from_pdf(file_path)
        if pdf_text:
            edited_file_stream = await analyze_and_edit(pdf_text, template_choice, language_choice)
            new_file_name = f"edited_{user_file_name.rsplit('.', 1)[0]}.docx"
            logger.info(f"PDF file edited: {new_file_name}")
    else:
        await update.message.reply_text(Reply.WRONG_EXT.value)
        os.remove(file_path)
        logger.warning(f"Unsupported file type: {document.mime_type}")
        return

    if edited_file_stream:
        await update.message.reply_document(
            document=edited_file_stream,
            filename=new_file_name,
            caption=Reply.SUCCESS.value
        )
        logger.info("Edited file sent to user.")
    else:
        await update.message.reply_text(Reply.COMPATIBLE.value)
        logger.warning("File could not be edited.")

    os.remove(file_path)
    logger.info(f"Temporary file {file_path} removed.")
