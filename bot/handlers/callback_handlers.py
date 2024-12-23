from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from common.enums import Button, Callback, Reply
from handlers.command_handlers import start_bot, stop_bot


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query is None:
        return

    await query.answer()

    return_button = [
        [InlineKeyboardButton(
                Button.BACK.value,
                callback_data=Callback.RETURN_TO_START.value
        )]
    ]
    return_markup = InlineKeyboardMarkup(return_button)

    handlers = {
        Callback.EDIT_CV.value: lambda: query.edit_message_text(
            Reply.EDIT_CV.value, reply_markup=return_markup
        ),
        'option_2': lambda: query.edit_message_text(
            'Вы выбрали: NA. Сделайте то-то и то-то',
            reply_markup=return_markup
        ),
        Callback.RETURN_TO_START.value: lambda: start_bot(update, context),
        Callback.STOP_BOT.value: lambda: stop_bot(update, context),
    }

    handler = handlers.get(query.data)
    if handler:
        await handler()
    else:
        await query.edit_message_text(
            Reply.NOT_EXIST.value.format(query=query.data),
            reply_markup=return_markup
        )
