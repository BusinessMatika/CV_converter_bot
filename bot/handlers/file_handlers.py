import os

from telegram import Update
from telegram.ext import ContextTypes

from common.constants import DOCX_MIME_TYPE
from common.enums import Reply
from utils.openai_utils import analyze_and_edit


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Save the received file
    document = update.message.document
    user_file_name = document.file_name  # название файла пользователя
    if document.mime_type != DOCX_MIME_TYPE:
        await update.message.reply_text(Reply.WRONG_EXT.value)
        return

    file_path = f'{user_file_name}'
    file = await context.bot.get_file(document.file_id)
    await file.download_to_drive(file_path)

    edited_file_path = await analyze_and_edit(file_path)

    if edited_file_path:
        await update.message.reply_document(
            document=open(edited_file_path, 'rb'),
            caption=Reply.SUCCESS.value
        )
    else:
        await update.message.reply_text(Reply.COMPATIBLE.value)

    os.remove(file_path)
    if os.path.exists(edited_file_path):
        os.remove(edited_file_path)
