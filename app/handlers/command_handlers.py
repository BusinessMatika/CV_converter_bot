from telegram import Update
from telegram.ext import ContextTypes

from app.common.constants import HELP_MESSAGE, START_MESSAGE, STOP_MESSAGE
from app.common.enums import Callback
from app.config import ADMIN_ID, DEBUG, logger
from app.permissions.permissions import (is_admin, require_admin,
                                         require_permission)
from app.utils.bot_utils import reset_state, send_message_or_edit_text
from app.utils.keyboard import admin_markup, main_menu_markup, return_back


@require_permission
async def start_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    reset_state(user_id, context)

    await send_message_or_edit_text(
        update, context,
        START_MESSAGE.format(first_name=user.first_name),
        reply_markup=main_menu_markup()
    )
    logger.info('Start bot message sent.')


@require_permission
async def stop_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    reset_state(user_id, context)
    if context.user_data is not None:
        context.user_data.clear()
    await send_message_or_edit_text(update, context, STOP_MESSAGE)
    logger.info('Stop bot message sent.')


@require_permission
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    reset_state(user_id, context)
    help_text = HELP_MESSAGE

    # Проверяем, является ли пользователь админом
    if is_admin(user_id, context):
        # Разбиваем HELP_MESSAGE, убираем последнюю строку
        help_lines = help_text.strip().split("\n")
        last_line = help_lines.pop()
        help_lines.append("🔧 <b><u>Команды для админа:</u></b>\n")
        help_lines.append("/manage_users - Управление пользователями.\n")
        help_lines.append(last_line)
        help_text = "\n".join(help_lines)

    message = update.message
    if message:
        await message.reply_text(
            text=help_text,
            parse_mode='HTML',
            reply_markup=return_back()
        )
        logger.info('Help message sent.')
    else:
        logger.warning('Help message not sent - message is None.')


@require_permission
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Эта команда отсутствует.'
    )
    logger.info('Unknown command response sent.')


@require_admin
async def manage_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Админ-команда для управления пользователями."""
    await send_message_or_edit_text(update, context, 'Выберите действие:', reply_markup=admin_markup())
