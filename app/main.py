import asyncio
import json
from typing import Any, Dict, Optional

from telegram import Update
from telegram.error import BadRequest
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          MessageHandler, filters)

from app.common.constants import ALLOWED_LANGUAGES, ALLOWED_TEMPLATES
from app.common.enums import Handler
from app.config import TELEGRAM_TOKEN, logger
from app.handlers.callback_handlers import handle_callback
from app.handlers.command_handlers import (help_command, start_bot, stop_bot,
                                           unknown)
from app.utils.bot_utils import update_language_choice, update_template_choice

from .handlers.file_handlers import handle_file


async def process_event(
        event: dict[str, Any], template: Optional[str], language: Optional[str]
) -> None:
    """Process a Telegram event and applies the appropriate handlers."""
    if not TELEGRAM_TOKEN:
        logger.error('TELEGRAM_TOKEN is not set.')
        raise ValueError("TELEGRAM_TOKEN is not set.")

    application = Application.builder().token(TELEGRAM_TOKEN).build()
    await application.initialize()

    handlers = [
        CommandHandler(Handler.START.value, start_bot),
        CommandHandler(Handler.HELP.value, help_command),
        CommandHandler(Handler.STOP.value, stop_bot),
        MessageHandler(
            filters.Document.ALL, lambda update, context: handle_file(
                update, context, template, language
            )
        ),
        CallbackQueryHandler(handle_callback),
        MessageHandler(filters.COMMAND, unknown)
    ]

    for handler in handlers:
        application.add_handler(handler)

    try:
        update = Update.de_json(json.loads(event["body"]), application.bot)
        await application.process_update(update)
    except BadRequest as e:
        logger.error(f"BadRequest Error: {e}")
    except Exception as e:
        logger.error(f"Unhandled Exception: {e}")


def lambda_handler(event: dict[str, Any], context: Any) -> Dict[str, Any]:
    """Lambda function to process events from SQS and forward to Telegram."""
    message = json.loads(event['Records'][0]['body'])

    template_data, language_data = None, None
    if 'body' in message:
        body_content = json.loads(message['body'])
        callback_query = body_content.get('callback_query')
        #
        if callback_query:
            data = callback_query.get('data')
            user_id = str(callback_query['from']['id'])
            if data in ALLOWED_LANGUAGES:
                language_data = data
                update_language_choice(user_id, language_data)
                logger.info(f'Language choice {language_data} updated for user {user_id}.')
            elif data in ALLOWED_TEMPLATES:
                template_data = data
                update_template_choice(user_id, template_data)
                logger.info(f'Template choice {template_data} updated for user {user_id}.')

    else:
        logger.error('No body found in message.')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        process_event(message, template_data, language_data)
    )
    return {
        'statusCode': 200,
        'body': json.dumps({'status': 'processed'})
    }
