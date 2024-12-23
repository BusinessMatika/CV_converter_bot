import os

from telegram import Update
from telegram.ext import ContextTypes

from common.constants import DOCX_MIME_TYPE
from common.enums import Reply
from utils.openai_utils import analyze_and_edit


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the file received from the user, processes it,
    and sends back the edited document.
    """
    # Retrieve the document from the update
    document = update.message.document
    user_file_name = document.file_name

    # Validate the file type
    if document.mime_type != DOCX_MIME_TYPE:
        await update.message.reply_text(Reply.WRONG_EXT.value)
        return

    # Save the received file
    file_path = f'{user_file_name}'
    file = await context.bot.get_file(document.file_id)
    await file.download_to_drive(file_path)

    # Process the file and get the edited stream
    edited_file_stream = await analyze_and_edit(file_path)

    if edited_file_stream:
        await update.message.reply_document(
            document=edited_file_stream,
            filename=f'edited_{user_file_name}',
            caption=Reply.SUCCESS.value
        )
    else:
        await update.message.reply_text(Reply.COMPATIBLE.value)

    os.remove(file_path)
