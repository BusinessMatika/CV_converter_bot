from typing import Optional, Union

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.common.enums import Button, Callback


def return_back(
    return_step: Optional[str] = None,
    as_markup: bool = True
) -> Union[list[InlineKeyboardButton], InlineKeyboardMarkup]:

    if return_step is None:
        return_step = Callback.RETURN_TO_START.value

    return_button = [
        [InlineKeyboardButton(Button.BACK.value, callback_data=return_step)]
    ]

    if as_markup:
        return InlineKeyboardMarkup(return_button)
    return return_button


def main_menu_markup(return_step: Optional[str] = None):
    keyboard = [
        [InlineKeyboardButton(
            Button.EDIT_CV.value, callback_data=Callback.EDIT_CV.value
        )],
        [InlineKeyboardButton(
            Button.CV_EVALUATION.value, callback_data=Callback.CV_EVALUATION.value
        )],
        [InlineKeyboardButton('3️⃣ NA', callback_data='option_3')],
        [InlineKeyboardButton('4️⃣ NA', callback_data='option_4')],
        [InlineKeyboardButton('5️⃣ NA', callback_data='option_5')],
        [InlineKeyboardButton('6️⃣ NA', callback_data='option_6')],
        [InlineKeyboardButton(
            Button.STOP.value, callback_data=Callback.STOP_BOT.value
        )]
    ]
    if return_step:
        keyboard.extend(return_back(return_step, False))
    return InlineKeyboardMarkup(keyboard)


def chosen_CV_language(return_step: Optional[str] = None):
    keyboard = [
        [InlineKeyboardButton(
            Button.RUSSIAN.value, callback_data=Callback.RUSSIAN.value)],
        [InlineKeyboardButton(
            Button.ENGLISH.value, callback_data=Callback.ENGLISH.value)]
    ]
    if return_step:
        keyboard.extend(return_back(return_step, False))
    return InlineKeyboardMarkup(keyboard)


def chosen_template_markup(return_step: Optional[str] = None):
    keyboard = [
        [InlineKeyboardButton(
            Button.BUSINESSMARIKA.value, callback_data=Callback.BUSINESSMATIKA.value)],
        [InlineKeyboardButton(
            Button.HUNTERCORE.value, callback_data=Callback.HUNTERCORE.value)],
        [InlineKeyboardButton(
            Button.TELESCOPE.value, callback_data=Callback.TELESCOPE.value)]
    ]
    if return_step:
        keyboard.extend(return_back(return_step, False))
    return InlineKeyboardMarkup(keyboard)


def admin_markup():
    keyboard = [
        [InlineKeyboardButton('➕ Добавить пользователя', callback_data='add_user')],
        [InlineKeyboardButton('➖ Удалить пользователя', callback_data='delete_user')],
        [InlineKeyboardButton(Button.BACK.value, callback_data=Callback.RETURN_TO_START.value)]

    ]
    return InlineKeyboardMarkup(keyboard)


def confirmation_add_markup(return_step: str):
    keyboard = [
        [InlineKeyboardButton("✅ Да", callback_data="confirm_add_user")],
        [InlineKeyboardButton("❌ Нет", callback_data="cancel_add_user")],
        [InlineKeyboardButton(Button.BACK.value, callback_data=return_step)]
    ]
    return InlineKeyboardMarkup(keyboard)


def confirmation_delete_markup(return_step: str):
    keyboard = [
        [InlineKeyboardButton("✅ Да", callback_data="confirm_delete_user")],
        [InlineKeyboardButton("❌ Нет", callback_data="cancel_delete_user")],
        [InlineKeyboardButton(Button.BACK.value, callback_data=return_step)]
    ]
    return InlineKeyboardMarkup(keyboard)
