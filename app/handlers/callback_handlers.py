from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.common.constants import ALLOWED_TEMPLATES
from app.common.enums import Button, Callback, CVTemplate, Reply
from app.config import DEBUG, logger
from app.handlers.command_handlers import start_bot, stop_bot
from app.utils.bot_utils import (send_message_or_edit_text,
                                 update_template_choice)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = str(query.from_user.id)
    if (template_choice := data) in ALLOWED_TEMPLATES:
        logger.info(
            f'User {user_id} choose one of templates: {template_choice}.')
        if not DEBUG:
            update_template_choice(user_id, template_choice)
            logger.info(
                f'Template {template_choice} updated in DB by user {user_id}.')

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
            update, context, Reply.EDIT_CV.value, reply_markup=template_selection_markup,
            parse_mode='HTML'
        ),
        Callback.BUSINESSMATIKA.value: lambda update, context: send_message_or_edit_text(
            update, context,
            Reply.TEMPLATE_CHOICE.value.format(
                template=CVTemplate.BUSINESSMATIKA.value.title()
            ),
            reply_markup=step_back_markup,
            parse_mode='HTML'
        ),
        Callback.HUNTERCORE.value: lambda update, context: send_message_or_edit_text(
            update, context, Reply.TEMPLATE_CHOICE.value.format(
                template=CVTemplate.HUNTERCORE.value.title()
            ),
            reply_markup=step_back_markup,
            parse_mode='HTML'
        ),
        Callback.TELESCOPE.value: lambda update, context: send_message_or_edit_text(
            update, context, Reply.TEMPLATE_CHOICE.value.format(
                template=CVTemplate.TELESCOPE.value.title()
            ),
            reply_markup=step_back_markup,
            parse_mode='HTML'
        ),
        'option_2': lambda update, context: send_message_or_edit_text(
            update, context, 'Вы выбрали: NA. Сделайте то-то и то-то',
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
