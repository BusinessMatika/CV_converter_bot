from functools import wraps

from telegram.ext import ContextTypes

from app.config import ADMIN_ID
from app.utils.bot_utils import (get_user_data, send_message_or_edit_text,
                                 table_telegram_users)


def is_allowed(user_id: int) -> bool:    
    return get_user_data(user_id, 'user_id', None, table_telegram_users)


def require_permission(func):
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user_id = str(update.effective_user.id)
        if not is_allowed(user_id):
            if is_admin(user_id, context):
                return await func(update, context, *args, **kwargs)
            await send_message_or_edit_text(update, context, 'Доступ запрещён')
            return
        return await func(update, context, *args, **kwargs)
    return wrapper


def is_admin(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    return user_id == ADMIN_ID


def require_admin(func):
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user_id = str(update.effective_user.id)
        if not is_admin(user_id, context):
            await send_message_or_edit_text(update, context, '⛔ У вас нет прав для выполнения этой команды.')
            return
        return await func(update, context, *args, **kwargs)
    return wrapper
