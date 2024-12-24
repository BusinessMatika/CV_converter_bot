import logging

from telegram.error import NetworkError, RetryAfter
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          MessageHandler, filters)

from common.constants import LOG_FORMAT
from common.enums import Handler
from config import TELEGRAM_TOKEN
from handlers.callback_handlers import handle_callback
from handlers.command_handlers import (help_command, start_bot, stop_bot,
                                       unknown)
from handlers.file_handlers import handle_file

logging.basicConfig(
    format=LOG_FORMAT,
    level=logging.INFO
)


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    handlers = [
        CommandHandler(Handler.START.value, start_bot),
        CommandHandler(Handler.HELP.value, help_command),
        CommandHandler(Handler.STOP.value, stop_bot),
        MessageHandler(filters.Document.DOCX, handle_file),
        CallbackQueryHandler(handle_callback),
        MessageHandler(filters.COMMAND, unknown)
    ]

    for handler in handlers:
        app.add_handler(handler)

    try:
        app.run_polling(poll_interval=0)
    except (NetworkError, RetryAfter) as e:
        print(f'Network error occurred: {e}')


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
