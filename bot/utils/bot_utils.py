async def send_message_or_edit_text(update, message, markup=None):

    if update.message:  # Если это команда /<название_команды>
        await update.message.reply_text(
            message,
            reply_markup=markup
        )
    elif update.callback_query:  # Если вызвано из кнопки <название_кнопки>
        query = update.callback_query
        await query.edit_message_text(
            text=message,
            reply_markup=markup
        )
