from telegram import Update
from telegram.ext import CallbackContext, ContextTypes

from app.common.constants import (ALLOWED_COMMANDS, ALLOWED_LANGUAGES,
                                  ALLOWED_TEMPLATES, FOR_ADMIN, MAX_LENGTH)
from app.config import (DEBUG, EDIT_CV_DB, EVALUATE_VAC_CV_DB,
                        TELEGRAM_STATE_DB, TELEGRAM_USERS_DB, logger)

if not DEBUG:
    import boto3
    dynamodb = boto3.resource('dynamodb')
    table_edit_cv = dynamodb.Table(EDIT_CV_DB)
    table_evaluate_vac_cv = dynamodb.Table(EVALUATE_VAC_CV_DB)
    table_telegram_users = dynamodb.Table(TELEGRAM_USERS_DB)
    table_states = dynamodb.Table(TELEGRAM_STATE_DB)
else:
    table_edit_cv = None
    table_evaluate_vac_cv = None
    table_telegram_users = None
    table_states = None


def update_user_data(
        user_id, field_name, value,
        context: CallbackContext, table
):
    """Update certain field in storage."""
    try:
        if DEBUG:
            context.user_data[field_name] = value
            return value
        else:
            response = table.update_item(
                Key={'user_id': user_id},
                UpdateExpression=f"SET {field_name} = :val",
                ExpressionAttributeValues={':val': value},
                ReturnValues="ALL_NEW"
            )
            logger.info(f"Table {table.name} update {field_name} succeeded: {response}")
            return response
    except Exception as e:
        logger.error(f"Error updating {field_name}: {str(e)}")
        return None


def get_user_data(user_id, field_name, context: CallbackContext, table):
    """Get certain field from storage."""
    try:
        if DEBUG:
            return context.user_data.get(field_name, None)
        else:
            response = table.get_item(Key={'user_id': user_id})
            if 'Item' in response:
                return response['Item'].get(field_name, None)
            else:
                logger.info(f"No {field_name} found for {user_id}")
                return None
    except Exception as e:
        logger.error(f"Error getting {field_name}: {str(e)}")
        return None
    

def delete_temporary_user_id(user_id: str):
    """Удаляет temporary_user_id у пользователя в DynamoDB."""
    response = table_telegram_users.update_item(
        Key={'user_id': user_id},
        UpdateExpression="REMOVE temporary_user_id",
        ConditionExpression="attribute_exists(temporary_user_id)",
        ReturnValues="UPDATED_NEW"
    )
    return response


def user_exists(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if DEBUG:
        return user_id in context.user_data.get('allowed_users', set())
    response = table_telegram_users.get_item(Key={'user_id': user_id})
    return 'Item' in response


def add_user_to_db(user_id: int, context: ContextTypes.DEFAULT_TYPE):
    if DEBUG:
        context.user_data.setdefault('allowed_users', set()).add(user_id)
    else:
        table_telegram_users.put_item(Item={'user_id': user_id})


def delete_user_from_db(user_id: int, context: ContextTypes.DEFAULT_TYPE):
    if DEBUG:
        context.user_data.setdefault('allowed_users', set()).discard(user_id)
    else:
        table_telegram_users.delete_item(Key={'user_id': user_id})


def update_vacancy(user_id, vacancy, context: CallbackContext):
    return update_user_data(user_id, 'vacancy', vacancy, context, table_evaluate_vac_cv)


def get_vacancy(user_id, context: CallbackContext):
    return get_user_data(user_id, 'vacancy', context, table_evaluate_vac_cv)


def update_state(user_id, state, context: CallbackContext):
    return update_user_data(user_id, 'current_state', state, context, table_states)


def reset_state(user_id, context: CallbackContext):
    update_user_data(user_id, 'current_state', None, context, table_states)
    logger.info(f'State обнулён: {get_state(user_id, context)}')


def get_state(user_id, context: CallbackContext):
    return get_user_data(user_id, 'current_state', context, table_states)


def update_language_choice(user_id, language_choice, context: CallbackContext):
    return update_user_data(user_id, 'language_choice', language_choice, context, table_edit_cv)


def get_user_language_choice(user_id, context: CallbackContext):
    return get_user_data(user_id, 'language_choice', context, table_edit_cv)


def update_template_choice(user_id, template_choice, context: CallbackContext):
    return update_user_data(user_id, 'template_choice', template_choice, context, table_edit_cv)


def get_user_template_choice(user_id, context: CallbackContext):
    return get_user_data(user_id, 'template_choice', context, table_edit_cv)


async def send_message_or_edit_text(update, context, message, reply_markup=None, parse_mode=None):
    # if command is /<command_name>.
    if update.message:
        await update.message.reply_text(
            message,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
    # If button <button_name> is pressed.
    elif update.callback_query:
        # For local develop usage only!
        if DEBUG:
            if update.callback_query.data in ALLOWED_TEMPLATES:
                context.user_data['template_choice'] = update.callback_query.data
            elif update.callback_query.data in ALLOWED_LANGUAGES:
                context.user_data['language_choice'] = update.callback_query.data
            elif update.callback_query.data in ALLOWED_COMMANDS:
                context.user_data['current_state'] = update.callback_query.data
            elif update.callback_query.data in FOR_ADMIN:
                context.user_data['current_state'] = update.callback_query.data
        query = update.callback_query
        await query.edit_message_text(
            text=message,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )


async def send_long_message(update: Update, text: str, parse_mode="HTML"):
    """
    Send message to user.
    If len(text) > 4096, messages will be split and sent separately.
    """
    for i in range(0, len(text), MAX_LENGTH):
        await update.message.reply_text(text[i:i + MAX_LENGTH], parse_mode=parse_mode)


async def validate_input(state: str, update: Update) -> bool:
    if state == 'waiting_for_cv':
        if not update.message.document:
            await update.message.reply_text('Пожалуйста, загрузите файл в формате ".docx" или ".pdf".')
            return False

    elif state == 'edit_cv':
        if not update.message.document and not update.callback_query:
            await update.message.reply_text('Пожалуйста, совершите одно из двух действий согласно инструкции: выберите команду на клавиатуре или загрузите файл.')
            return False
    return True
