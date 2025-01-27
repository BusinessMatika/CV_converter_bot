from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown

from app.common.constants import HELP_MESSAGE, START_MESSAGE, STOP_MESSAGE
from app.common.enums import Button, Callback
from app.config import DEBUG, logger
from app.utils.bot_utils import send_message_or_edit_text


async def start_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user is None:
        logger.warning("User is None in start_bot.")
        return

    keyboard = [
        [InlineKeyboardButton(
            Button.EDIT_CV.value, callback_data=Callback.EDIT_CV.value
        )],
        [InlineKeyboardButton('2️⃣ NA', callback_data='option_2')],
        [InlineKeyboardButton('3️⃣ NA', callback_data='option_3')],
        [InlineKeyboardButton('4️⃣ NA', callback_data='option_4')],
        [InlineKeyboardButton('5️⃣ NA', callback_data='option_5')],
        [InlineKeyboardButton('6️⃣ NA', callback_data='option_6')],
        [InlineKeyboardButton(
            Button.STOP.value, callback_data=Callback.STOP_BOT.value
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await send_message_or_edit_text(
        update, context,
        START_MESSAGE.format(first_name=user.first_name),
        reply_markup=reply_markup
    )
    logger.info("Start bot message sent.")
    logger.info(f'DEBUG = {DEBUG}')


async def stop_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Stop command received.")
    if context.user_data is not None:
        context.user_data.clear()
    await send_message_or_edit_text(update, context, STOP_MESSAGE)
    logger.info("Stop bot message sent.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Help command received.")
    help_text = HELP_MESSAGE
    return_button = [
        [InlineKeyboardButton(
            Button.BACK.value, callback_data=Callback.RETURN_TO_START.value
        )]
    ]
    return_markup = InlineKeyboardMarkup(return_button)

    message = update.message
    if message:
        await message.reply_text(
            text=help_text,
            parse_mode='HTML',
            reply_markup=return_markup
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
