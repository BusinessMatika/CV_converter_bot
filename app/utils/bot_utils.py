from app.common.constants import ALLOWED_LANGUAGES, ALLOWED_STATES, ALLOWED_TEMPLATES
from app.config import DEBUG, DynamoDB, logger

if not DEBUG:
    import boto3
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DynamoDB)


def update_state(user_id, state):
    try:
        response = table.update_item(
            Key={'user_id': user_id},
            UpdateExpression="SET command = :command",
            ExpressionAttributeValues={':command': state},
            ReturnValues="ALL_NEW"
        )
        logger.info(f"State update succeeded: {response}")
        return response
    except Exception as e:
        logger.error(f"Error updating state: {str(e)}")
        return None


def get_state(user_id):
    try:
        response = table.get_item(Key={'user_id': user_id})
        if 'Item' in response:
            return response['Item'].get('command', None)
        else:
            logger.info(f"No state found for {user_id}")
            return None
    except Exception as e:
        logger.error(f"Error getting state: {str(e)}")
        return None


def update_language_choice(user_id, language_choice):
    try:
        response = table.update_item(
            Key={'user_id': user_id},
            UpdateExpression="SET language_choice = :language_choice",
            ExpressionAttributeValues={':language_choice': language_choice},
            ReturnValues="ALL_NEW"
        )
        logger.info(f"Language update succeeded: {response}")
        return response
    except Exception as e:
        logger.error(f"Error updating language_choice: {str(e)}")
        return None


def get_user_language_choice(user_id):
    try:
        response = table.get_item(Key={'user_id': user_id})
        if 'Item' in response:
            return response['Item'].get('language_choice', None)
        else:
            logger.info(f"No language_choice found for {user_id}")
            return None
    except Exception as e:
        logger.error(f"Error getting language_choice: {str(e)}")
        return None


def update_template_choice(user_id, template_choice):
    try:
        response = table.update_item(
            Key={'user_id': user_id},
            UpdateExpression="SET template_choice = :template_choice",
            ExpressionAttributeValues={':template_choice': template_choice},
            ReturnValues="ALL_NEW"
        )
        logger.info(f"Update succeeded: {response}")
        return response
    except Exception as e:
        logger.error(f"Error updating template_choice: {str(e)}")
        return None


def get_user_template_choice(user_id):
    try:
        response = table.get_item(Key={'user_id': user_id})
        if 'Item' in response:
            return response['Item'].get('template_choice', None)
        else:
            logger.info(f"No template_choice found for {user_id}")
            return None
    except Exception as e:
        logger.error(f"Error getting template_choice: {str(e)}")
        return None


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
                context.user_data['cv_template'] = update.callback_query.data
            elif update.callback_query.data in ALLOWED_LANGUAGES:
                context.user_data['chosen_language'] = update.callback_query.data
            elif update.callback_query.data in ALLOWED_STATES:
                context.user_data['state'] = update.callback_query.data
        query = update.callback_query
        await query.edit_message_text(
            text=message,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
