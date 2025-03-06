from telegram import Update
from telegram.ext import ContextTypes

from app.common.constants import ALLOWED_LANGUAGES
from app.common.enums import Callback, CVTemplate, CVTranslation, Reply
from app.config import logger
from app.handlers.command_handlers import start_bot, stop_bot
from app.utils.bot_utils import (get_user_template_choice,
                                 send_message_or_edit_text)
from app.utils.keyboard import (chosen_CV_language, chosen_template_markup,
                                return_back)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = str(query.from_user.id)

    if data in ALLOWED_LANGUAGES:
        template_choice = get_user_template_choice(user_id, context)

    command_handlers = {
        Callback.EDIT_CV.value: lambda update, context: send_message_or_edit_text(
            update, context, Reply.EDIT_CV.value,
            reply_markup=chosen_template_markup(Callback.RETURN_TO_START.value),
            parse_mode='HTML'
        ),
        Callback.CV_EVALUATION.value: lambda update, context: send_message_or_edit_text(
            update, context, Reply.CV_EVALUATION.value,
            reply_markup=return_back(),
            parse_mode='HTML'
        )
    }

    template_handlers = {
        Callback.BUSINESSMATIKA.value: lambda update, context: send_message_or_edit_text(
            update, context,
            Reply.TEMPLATE_CHOICE.value.format(
                template=CVTemplate.BUSINESSMATIKA.value.title()
            ),
            reply_markup=chosen_CV_language(Callback.EDIT_CV.value),
            parse_mode='HTML'
        ),
        Callback.HUNTERCORE.value: lambda update, context: send_message_or_edit_text(
            update, context, Reply.TEMPLATE_CHOICE.value.format(
                template=CVTemplate.HUNTERCORE.value.title()
            ),
            reply_markup=chosen_CV_language(Callback.EDIT_CV.value),
            parse_mode='HTML'
        ),
        Callback.TELESCOPE.value: lambda update, context: send_message_or_edit_text(
            update, context, Reply.TEMPLATE_CHOICE.value.format(
                template=CVTemplate.TELESCOPE.value.title()
            ),
            reply_markup=chosen_CV_language(Callback.EDIT_CV.value),
            parse_mode='HTML'
        )
    }

    translation_handlers = {
        Callback.RUSSIAN.value: lambda update, context: send_message_or_edit_text(
            update, context, Reply.TRANSLATION_CHOICE.value.format(
                language=CVTranslation.RUSSIAN.value
            ), reply_markup=return_back(template_choice),
            parse_mode='HTML'
        ),
        Callback.ENGLISH.value: lambda update, context: send_message_or_edit_text(
            update, context, Reply.TRANSLATION_CHOICE.value.format(
                language=CVTranslation.ENGLISH.value
            ), reply_markup=return_back(template_choice),
            parse_mode='HTML'
        )
    }

    system_handlers = {
        Callback.RETURN_TO_START.value: lambda update, context: start_bot(update, context),
        Callback.STOP_BOT.value: lambda update, context: stop_bot(update, context),
    }

    handlers = {
        **command_handlers,
        **template_handlers,
        **translation_handlers,
        **system_handlers
    }

    handler = handlers.get(query.data)
    if handler:
        logger.info(f"Executing handler for {query.data}")
        await handler(update, context)
    else:
        logger.warning(f"No handler found for {query.data}")
        await query.edit_message_text(
            Reply.NOT_EXIST.value.format(query=query.data),
            reply_markup=return_back(),
            parse_mode='HTML'
        )
