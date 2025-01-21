from app.common.enums import Reply


async def send_message_or_edit_text(update, message, reply_markup=None, parse_mode=None):
    # if command is /<command_name>.
    if update.message:
        await update.message.reply_text(
            message,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
    # If button <button_name> is pressed.
    elif update.callback_query:
        query = update.callback_query
        await query.edit_message_text(
            text=message,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )


async def update_template_choice(update, context, template_choice: str, reply_markup=None, parse_mode='HTML'):
    context.user_data['cv_format'] = template_choice
    await send_message_or_edit_text(
        update,
        message=Reply.TEMPLATE_CHOICE.value.format(template=template_choice.title()),
        reply_markup=reply_markup,
        parse_mode=parse_mode
    )
