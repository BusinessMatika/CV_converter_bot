from telegram import Update
from telegram.ext import ContextTypes

from app.common.constants import HELP_MESSAGE, START_MESSAGE, STOP_MESSAGE
from app.config import DEBUG, logger
from app.utils.bot_utils import reset_state, send_message_or_edit_text
from app.utils.keyboard import main_menu_markup, return_back


async def start_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    if user is None:
        logger.warning('User is None in start_bot.')
        return
    reset_state(user_id, context)

    await send_message_or_edit_text(
        update, context,
        START_MESSAGE.format(first_name=user.first_name),
        reply_markup=main_menu_markup()
    )
    logger.info("Start bot message sent.")


async def stop_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    reset_state(user_id, context)
    if context.user_data is not None:
        context.user_data.clear()
    await send_message_or_edit_text(update, context, STOP_MESSAGE)
    logger.info("Stop bot message sent.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    reset_state(user_id, context)
    help_text = HELP_MESSAGE

    message = update.message
    if message:
        await message.reply_text(
            text=help_text,
            parse_mode='HTML',
            reply_markup=return_back()
        )
        logger.info("Help message sent.")
    else:
        logger.warning("Help message not sent - message is None.")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Эта команда отсутствует."
    )
    logger.info("Unknown command response sent.")
