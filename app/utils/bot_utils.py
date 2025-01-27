from app.common.constants import ALLOWED_TEMPLATES
from app.config import DEBUG, DynamoDB, logger

if not DEBUG:
    import boto3
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DynamoDB)


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
        if DEBUG and update.callback_query.data in ALLOWED_TEMPLATES:
            context.user_data['cv_template'] = update.callback_query.data
        query = update.callback_query
        await query.edit_message_text(
            text=message,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
