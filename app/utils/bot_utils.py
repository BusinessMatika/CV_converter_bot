async def send_message_or_edit_text(update, message, markup=None):
    # if command is /<command_name>.
    if update.message:
        await update.message.reply_text(
            message,
            reply_markup=markup
        )
    # If button <button_name> is pressed.
    elif update.callback_query:
        query = update.callback_query
        await query.edit_message_text(
            text=message,
            reply_markup=markup
        )
