from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from common.enums import Button, Callback, Reply
from handlers.command_handlers import start_bot, stop_bot


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == Callback.EDIT_CV.value:
        return_button = [
            [InlineKeyboardButton(
                Button.BACK.value, callback_data=Callback.RETURN_TO_START.value
            )]
        ]
        return_markup = InlineKeyboardMarkup(return_button)

        await query.edit_message_text(
            Reply.EDIT_CV.value,
            reply_markup=return_markup
        )

    # # ВРЕМЕННОЕ РЕШЕНИЕ ДЛЯ ПРОВЕРКИ!!!
    # elif query.data == 'option_2':
    #     # Кнопка 'Назад'
    #     return_button = [
    #         [InlineKeyboardButton(
    #             Button.BACK.value, callback_data=Callback.RETURN_TO_START.value
    #         )]
    #     ]
    #     return_markup = InlineKeyboardMarkup(return_button)

    #     await query.edit_message_text(
    #         'Вы выбрали: NA. Сделайте то-то и то-то',
    #         reply_markup=return_markup
    #     )

    elif query.data == Callback.RETURN_TO_START.value:
        await start_bot(update, context)

    elif query.data == Callback.STOP_BOT.value:
        await stop_bot(update, context)

    else:
        return_button = [
            [InlineKeyboardButton(
                Button.BACK.value, callback_data=Callback.RETURN_TO_START.value
            )]
        ]
        return_markup = InlineKeyboardMarkup(return_button)
        await query.edit_message_text(
            Reply.NOT_EXIST.value.format(query=query.data),
            reply_markup=return_markup
        )