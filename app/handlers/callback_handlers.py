from telegram import Update
from telegram.ext import ContextTypes

from app.common.constants import ALLOWED_LANGUAGES
from app.common.enums import Callback, CVTemplate, CVTranslation, Reply
from app.config import logger
from app.handlers.command_handlers import manage_users, start_bot, stop_bot
from app.permissions.permissions import require_permission
from app.utils.bot_utils import (add_user_to_db, delete_temporary_user_id, delete_user_from_db,
                                 get_state, get_user_data,
                                 get_user_template_choice,
                                 send_message_or_edit_text,
                                 table_telegram_users)
from app.utils.keyboard import (chosen_CV_language, chosen_template_markup,
                                return_back)


@require_permission
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gateway to handle all callbacks."""
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
            ), reply_markup=return_back(return_step=template_choice),
            parse_mode='HTML'
        ),
        Callback.ENGLISH.value: lambda update, context: send_message_or_edit_text(
            update, context, Reply.TRANSLATION_CHOICE.value.format(
                language=CVTranslation.ENGLISH.value
            ), reply_markup=return_back(return_step=template_choice),
            parse_mode='HTML'
        )
    }

    system_handlers = {
        Callback.RETURN_TO_START.value: lambda update, context: start_bot(update, context),
        Callback.STOP_BOT.value: lambda update, context: stop_bot(update, context),
    }

    admin_handlers = {
        'add_user': lambda update, context: send_message_or_edit_text(
            update, context, 'Напишите id пользователя для добавления',
            reply_markup=return_back(return_step='manage_users')
        ),
        'delete_user': lambda update, context: send_message_or_edit_text(
            update, context, 'Напишите id пользователя для удаления',
            reply_markup=return_back(return_step='manage_users')
        ),
        'manage_users': lambda update, context: manage_users(update, context),
        'confirm_add_user': lambda update, context: confirm_add_user(update, context),
        'confirm_delete_user': lambda update, context: confirm_delete_user(update, context),
        'cancel_add_user': lambda update, context: cancel_add_user(update, context), #manage_users(update, context)
        'cancel_delete_user': lambda update, context: cancel_delete_user(update, context)
    }


    handlers = {
        **command_handlers,
        **template_handlers,
        **translation_handlers,
        **system_handlers,
        **admin_handlers
    }

    handler = handlers.get(data)
    if handler:
        logger.info(f"Executing handler for {data}")
        await handler(update, context)
    else:
        logger.warning(f"No handler found for {data}")
        await query.edit_message_text(
            Reply.NOT_EXIST.value.format(query=data),
            reply_markup=return_back(),
            parse_mode='HTML'
        )


async def confirm_add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    new_user_id = get_user_data(user_id, 'temporary_user_id', context, table_telegram_users)
    state = get_state(user_id, context)

    if not new_user_id:
        await send_message_or_edit_text(update, context, "Ошибка: не найден ID пользователя для добавления.")
        return

    add_user_to_db(new_user_id, context)
    delete_temporary_user_id(user_id)
    await send_message_or_edit_text(update, context, f"Пользователь {new_user_id} успешно добавлен.", reply_markup=return_back(state))


async def cancel_add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    new_user_id = get_user_data(user_id, 'temporary_user_id', context, table_telegram_users)
    if not new_user_id:
        await send_message_or_edit_text(update, context, f"Отмена операции добавления. ID пользователя {new_user_id} не найден.", reply_markup=return_back(state))
        return
    state = get_state(user_id, context)
    delete_temporary_user_id(user_id)
    await send_message_or_edit_text(update, context, f'Вы отменили операцию добавления пользователя {new_user_id}', reply_markup=return_back(state))


async def confirm_delete_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    delete_user_id = get_user_data(user_id, 'temporary_user_id', context, table_telegram_users)
    state = get_state(user_id, context)

    if not delete_user_id:
        await send_message_or_edit_text(update, context, "Ошибка: не найден ID пользователя для добавления.", reply_markup=return_back(state))
        return

    delete_user_from_db(delete_user_id, context)
    delete_temporary_user_id(user_id)
    await send_message_or_edit_text(update, context, f"Пользователь {delete_user_id} успешно удалён.", reply_markup=return_back(state))


async def cancel_delete_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    delete_user_id = get_user_data(user_id, 'temporary_user_id', context, table_telegram_users)
    if not delete_user_id:
        await send_message_or_edit_text(update, context, f"Отмена операции удаления. ID пользователя {delete_user_id} не найден.", reply_markup=return_back(state))
        return
    state = get_state(user_id, context)
    delete_temporary_user_id(user_id)
    await send_message_or_edit_text(update, context, f'Вы отменили операцию удаления пользователя {delete_user_id}', reply_markup=return_back(state))