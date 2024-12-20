from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown

from common.constants import HELP_MESSAGE, START_MESSAGE, STOP_MESSAGE
from common.enums import Button, Callback
from utils.bot_utils import send_message_or_edit_text


async def start_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user is None:
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
        update,
        START_MESSAGE.format(first_name=user.first_name),
        markup=reply_markup
    )


async def stop_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await send_message_or_edit_text(update, STOP_MESSAGE)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = HELP_MESSAGE
    return_button = [
        [InlineKeyboardButton(
            Button.BACK.value, callback_data=Callback.RETURN_TO_START.value
        )]
    ]
    return_markup = InlineKeyboardMarkup(return_button)

    await update.message.reply_text(
        text=escape_markdown(help_text, version=2),
        parse_mode='MarkdownV2',
        reply_markup=return_markup
    )
