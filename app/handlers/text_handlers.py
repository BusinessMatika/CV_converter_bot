from telegram import Update
from telegram.ext import ContextTypes

from app.config import logger
from app.handlers.file_handlers import handle_cv_evaluation
from app.permissions.permissions import is_admin, require_permission
from app.utils.bot_utils import (get_state, table_telegram_users,
                                 update_user_data, user_exists)
from app.utils.keyboard import (confirmation_add_markup,
                                confirmation_delete_markup)


@require_permission
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages based on state."""
    user_id = str(update.effective_user.id)
    state = get_state(user_id, context)

    if not state:
        await update.message.reply_text("Я вас не понимаю. Введите команду или используйте кнопки меню.")
        return

    if state == 'cv_evaluation':
        await handle_cv_evaluation(update, context)
    elif state == 'add_user':
        if not is_admin(user_id, context):
            await update.message.reply_text("У вас нет прав для добавления пользователей.")
            return

        new_user_id = update.message.text.strip()
        if user_exists(new_user_id, context):
            await update.message.reply_text(f"Пользователь {new_user_id} уже существует в базе.")
            return

        update_user_data(user_id, 'temporary_user_id', new_user_id, context, table_telegram_users)
        await update.message.reply_text(
            f'Подтвердите добавление пользователя с id {new_user_id}', reply_markup=confirmation_add_markup(return_step=state)
        )


    elif state == 'delete_user':
        if not is_admin(user_id, context):
            await update.message.reply_text("У вас нет прав для удаления пользователей.")
            return

        delete_user_id = update.message.text.strip()
        if not user_exists(delete_user_id, context):
            await update.message.reply_text(f"Пользователь с id {delete_user_id} не существует в базе.")
            return

        update_user_data(user_id, 'temporary_user_id', delete_user_id, context, table_telegram_users)
        await update.message.reply_text(
            f'Подтвердите удаление пользователя с id {delete_user_id}', reply_markup=confirmation_delete_markup(return_step=state)
        )

    else:
        await update.message.reply_text("Неизвестная команда. Попробуйте снова.")
