import asyncio
import json

from telegram import Update
from telegram.error import BadRequest
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          MessageHandler, filters)

from app.config import TELEGRAM_TOKEN
from app.handlers.callback_handlers import handle_callback
from app.handlers.command_handlers import (help_command, start_bot, stop_bot,
                                           unknown)

from .handlers.file_handlers import handle_file


async def process_event(event):
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    await application.initialize()

    handlers = [
        CommandHandler("start", start_bot),
        CommandHandler("help", help_command),
        CommandHandler("stop", stop_bot),
        MessageHandler(filters.Document.ALL, handle_file),
        CallbackQueryHandler(handle_callback),
        MessageHandler(filters.COMMAND, unknown)
    ]

    for handler in handlers:
        application.add_handler(handler)

    try:
        update = Update.de_json(json.loads(event["body"]), application.bot)
        await application.process_update(update)
    except BadRequest as e:
        print(f"BadRequest Error: {e}")
    except Exception as e:
        print(f"Unhandled Exception: {e}")


def lambda_handler(event, context):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        process_event(json.loads(event['Records'][0]['body']))
    )
    return {
        'statusCode': 200,
        'body': json.dumps({'status': 'processed'})
    }
