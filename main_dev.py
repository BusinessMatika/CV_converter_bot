import uvicorn
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          MessageHandler, filters)

from app.common.enums import Handler
from app.config import TELEGRAM_TOKEN
from app.handlers.callback_handlers import handle_callback
from app.handlers.command_handlers import (help_command, start_bot, stop_bot,
                                           unknown)
from app.handlers.file_handlers import handle_file

# Initialize the FastAPI app
fastapi_app = FastAPI()
cd 

async def main():
    # Initialize the Telegram bot application (initialize it correctly)
    telegram_app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Define the handlers
    handlers = [
        CommandHandler(Handler.START.value, start_bot),
        CommandHandler(Handler.HELP.value, help_command),
        CommandHandler(Handler.STOP.value, stop_bot),
        MessageHandler(filters.Document.ALL, handle_file),
        CallbackQueryHandler(handle_callback),
        MessageHandler(filters.COMMAND, unknown)
    ]

    # Add handlers to the Telegram application
    for handler in handlers:
        telegram_app.add_handler(handler)

    await telegram_app.bot.set_webhook(
        url='https://5109-82-215-113-60.ngrok-free.app/webhook',
        allowed_updates=Update.ALL_TYPES
    )

    # Define the webhook route in FastAPI
    @fastapi_app.post("/webhook")
    async def handle_webhook(request: Request):
        data = await request.json()
        # Parse the incoming request
        update = Update.de_json(data=data, bot=telegram_app.bot)
        # Process the update using the Telegram application
        await telegram_app.update_queue.put(update)
        return {"status": "ok"}
    
    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app=fastapi_app,
            port=8443,
            use_colors=False,
            host='0.0.0.0',
            forwarded_allow_ips='*',
            proxy_headers=True,
        ),
    )

    async with telegram_app:
        await telegram_app.start()
        await webserver.serve()
        await telegram_app.stop()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())