from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.common.enums import Button, Callback, CVTemplate, Reply
from app.config import logger
from app.handlers.command_handlers import start_bot, stop_bot
from app.utils.bot_utils import (send_message_or_edit_text,
                                 update_template_choice)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    return_button = [
        [InlineKeyboardButton(
                Button.BACK.value,
                callback_data=Callback.RETURN_TO_START.value
        )]
    ]
    return_markup = InlineKeyboardMarkup(return_button)

    step_back_button = [
        [InlineKeyboardButton(
            Button.BACK.value,
            callback_data=Callback.EDIT_CV.value
        )]
    ]
    step_back_markup = InlineKeyboardMarkup(step_back_button)

    template_selection_buttons = [
        [InlineKeyboardButton(
            Button.BUSINESSMARIKA.value, callback_data=Callback.BUSINESSMATIKA.value)],
        [InlineKeyboardButton(
            Button.HUNTERCORE.value, callback_data=Callback.HUNTERCORE.value)],
        [InlineKeyboardButton(
            Button.TELESCOPE.value, callback_data=Callback.TELESCOPE.value)],
        [InlineKeyboardButton(
            Button.BACK.value, callback_data=Callback.RETURN_TO_START.value)]
    ]
    template_selection_markup = InlineKeyboardMarkup(template_selection_buttons)

    handlers = {
        Callback.EDIT_CV.value: lambda update, context: send_message_or_edit_text(
            update, Reply.EDIT_CV.value, reply_markup=template_selection_markup,
            parse_mode='HTML'
        ),
        Callback.BUSINESSMATIKA.value: lambda update, context: update_template_choice(
            update, context, CVTemplate.BUSINESSMATIKA.value,
            reply_markup=step_back_markup
        ),
        Callback.HUNTERCORE.value: lambda update, context: update_template_choice(
            update, context, CVTemplate.HUNTERCORE.value,
            reply_markup=step_back_markup
        ),
        Callback.TELESCOPE.value: lambda update, context: update_template_choice(
            update, context, CVTemplate.TELESCOPE.value,
            reply_markup=step_back_markup
        ),
        'option_2': lambda update, context: send_message_or_edit_text(
            update, 'Вы выбрали: NA. Сделайте то-то и то-то',
            reply_markup=return_markup
        ),
        Callback.RETURN_TO_START.value: lambda update, context: start_bot(update, context),
        Callback.STOP_BOT.value: lambda update, context: stop_bot(update, context),
    }

    handler = handlers.get(query.data)
    if handler:
        logger.info(f"Executing handler for {query.data}")
        await handler(update, context)
    else:
        logger.warning(f"No handler found for {query.data}")
        await query.edit_message_text(
            Reply.NOT_EXIST.value.format(query=query.data),
            reply_markup=return_markup,
            parse_mode='HTML'
        )
