import io
import os
from typing import Optional

from telegram import Update
from telegram.ext import ContextTypes

from app.common.constants import (ALLOWED_LANGUAGES, DOCX_MIME_TYPE,
                                  PDF_MIME_TYPE)
from app.common.enums import Reply
from app.config import DEBUG, logger
from app.utils.bot_utils import (get_state, get_user_language_choice,
                                 get_user_template_choice, get_vacancy,
                                 send_long_message, send_message_or_edit_text,
                                 update_state, update_vacancy, validate_input)
from app.utils.docx_utils import extract_text_from_docx
from app.utils.openai_utils import (analyze_and_edit_cv, analyze_vacancy,
                                    analyze_vacancy_and_cv)
from app.utils.pdf_utils import extract_text_from_pdf


async def handle_file(
        update: Update, context: ContextTypes.DEFAULT_TYPE,
        template: Optional[str] = None,
        language: Optional[str] = None,
        state: Optional[str] = None
):
    user_id = str(update.message.from_user.id)
    state = context.user_data.get(
        'current_state') if DEBUG else get_state(user_id, context)

    if not state:
        await update.message.reply_text(
            'Я вас не понимаю. Введите команду или используйте кнопки меню.')
        return

    if not validate_input(state, update):
        return

    if state == 'edit_cv':
        await validate_input(state, update)
        await handle_edit_cv(update, context, template, language)
    elif state == 'cv_evaluation':
        await handle_cv_evaluation(update, context)
    elif state == 'waiting_for_cv':
        await validate_input(state, update)
        await handle_waiting_for_cv(update, context)
    else:
        await update.message.reply_text(
            'Неизвестная команда. Попробуйте снова.')


async def handle_cv_evaluation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'User {update.message.from_user.full_name} chose command cv_evaluation')
    vacancy_data = await evaluate_vacancy(update, context)
    user_id = str(update.message.from_user.id)

    if vacancy_data:
        update_vacancy(user_id, vacancy_data, context)
        update_state(user_id, 'waiting_for_cv', context)
        await update.message.reply_text('Вакансия принята! Теперь загрузите ваше резюме.')
    else:
        await update.message.reply_text('Ошибка обработки вакансии, попробуйте снова.')


async def evaluate_vacancy(
        update: Update, context: ContextTypes.DEFAULT_TYPE
):
    logger.info('Executing evaluate_vacancy')
    if vacancy := update.message.text: 
        evaluated_vacancy_stream = await analyze_vacancy(
            update, context, user_text=vacancy
        )
    elif update.message.document:
        vacancy_file = update.message.document
        vacancy_file_name = vacancy_file.file_name
        logger.info(f'Received vacancy: {vacancy_file_name}.')
        if DEBUG:
            vacancy_path = f'{vacancy_file_name}'
        else:
            vacancy_path = os.path.join('/tmp', vacancy_file_name)

        file = await context.bot.get_file(vacancy_file.file_id)
        await file.download_to_drive(vacancy_path)
        logger.info(f'Vacancy saved to {vacancy_path}')
        await send_message_or_edit_text(
            update,
            context,
            Reply.VACANCY_EVAL_EXECUTION.value.format(
                file_name=vacancy_file_name
            ),
            parse_mode='HTML'
        )

        if vacancy_file.mime_type == DOCX_MIME_TYPE:
            docx_text = extract_text_from_docx(vacancy_path)
            evaluated_vacancy_stream = await analyze_vacancy(
                update, context,
                docx_text
            )
            new_vacancy_file_name = f"evaluated_{vacancy_file_name}"
            logger.info(f"DOCX vacancy has been analyzed: {new_vacancy_file_name}")
        elif vacancy_file.mime_type == PDF_MIME_TYPE:
            pdf_text = extract_text_from_pdf(vacancy_path)
            if pdf_text:
                evaluated_vacancy_stream = await analyze_vacancy(
                    update, context,
                    pdf_text
                )
                new_vacancy_file_name = f"evaluated_{vacancy_file_name.rsplit('.', 1)[0]}.docx"
                logger.info(f"PDF vacancy has been analyzed: {new_vacancy_file_name}")
        else:
            await update.message.reply_text(Reply.WRONG_EXT.value)
            os.remove(vacancy_path)
            logger.warning(f"Unsupported file type: {vacancy_file.mime_type}")
            return

        os.remove(vacancy_path)
        logger.info(f"Temporary file {vacancy_path} removed.")
    return evaluated_vacancy_stream


async def handle_waiting_for_cv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'User {update.message.from_user.full_name} is uploading CV.')
    user_id = str(update.message.from_user.id)
    vacancy_data = get_vacancy(user_id, context)

    if vacancy_data:
        await evaluate_cv(update, context, vacancy_data)
    else:
        await update.message.reply_text("Ошибка! Вакансия не найдена. Начните заново с /cv_evaluation.")


async def evaluate_cv(
        update: Update, context: ContextTypes.DEFAULT_TYPE,
        vacancy_data
):
    if cv_file := update.message.document:
        cv_file_name = cv_file.file_name
        logger.info(f'Received CV: {cv_file_name}')
        if DEBUG:
            cv_path = f'{cv_file_name}'
        else:
            cv_path = os.path.join('/tmp', cv_file_name)

        file = await context.bot.get_file(cv_file.file_id)
        await file.download_to_drive(cv_path)
        logger.info(f'CV saved to {cv_path}')

        await send_message_or_edit_text(
            update,
            context,
            Reply.VACANCY_CV_EVAL_EXECUTION.value.format(
                file_name=cv_file_name
            ),
            parse_mode='HTML'
        )

        if cv_file.mime_type == DOCX_MIME_TYPE:
            docx_text = extract_text_from_docx(cv_path)
            evaluated_cv_stream = await analyze_vacancy_and_cv(
                update, context,
                docx_text,
                vacancy_data
            )
            new_cv_file_name = f"evaluated_{cv_file_name}"
            logger.info(f"DOCX cv has been analyzed: {new_cv_file_name}")
        elif cv_file.mime_type == PDF_MIME_TYPE:
            pdf_text = extract_text_from_pdf(cv_path)
            if pdf_text:
                evaluated_cv_stream = await analyze_vacancy_and_cv(
                    update, context,
                    pdf_text,
                    vacancy_data
                )
                new_cv_file_name = f"evaluated_{cv_file_name.rsplit('.', 1)[0]}.docx"
                logger.info(f"PDF cv has been analyzed: {new_cv_file_name}")
        else:
            await update.message.reply_text(Reply.WRONG_EXT.value)
            os.remove(cv_path)
            logger.warning(f"Unsupported file type: {cv_file.mime_type}")
            return
        await send_long_message(update, evaluated_cv_stream, parse_mode="HTML")
        logger.info("Evaluation sent to user.")

        os.remove(cv_path)
        logger.info(f"Temporary file {cv_path} removed.")


async def handle_edit_cv(update: Update, context: ContextTypes.DEFAULT_TYPE,
                         template: Optional[str] = None, language: Optional[str] = None):
    logger.info(f'User {update.message.from_user.full_name} chose command edit_cv')
    await edit_cv(update, context, template, language)


async def edit_cv(
        update: Update, context: ContextTypes.DEFAULT_TYPE,
        template=None, language=None
):
    """
    Handles the file received from the user, processes it,
    and sends back the edited document.
    """
    user_id = str(update.message.from_user.id)
    document = update.message.document
    user_file_name = document.file_name
    logger.info(f"Received file: {user_file_name}")

    template_choice = get_user_template_choice(user_id, context)
    language_choice = get_user_language_choice(user_id, context)
    logger.info(
        f'CV will be edited in accordance with template: {template_choice}. '
        f'CV language will be {language_choice}.'
    )
    file_path = f'{user_file_name}' if DEBUG else os.path.join(
        '/tmp', user_file_name)

    file = await context.bot.get_file(document.file_id)
    await file.download_to_drive(file_path)
    logger.info(f'CV saved to {file_path}')

    if language_choice:
        await send_message_or_edit_text(
            update,
            context,
            Reply.EDIT_CV_EXECUTION.value.format(
                file_name=user_file_name,
                template_name=template_choice.capitalize(),
                language_name=ALLOWED_LANGUAGES.get(language_choice)
            ),
            parse_mode='HTML'
        )

    if document.mime_type == DOCX_MIME_TYPE:
        docx_text = extract_text_from_docx(file_path)
        if docx_text:
            edited_file_stream = await analyze_and_edit_cv(
                update, context, template_choice,
                language_choice, docx_text
            )
            new_file_name = f"edited_{user_file_name}"
            logger.info(f"DOCX file edited: {new_file_name}")
    elif document.mime_type == PDF_MIME_TYPE:
        pdf_text = extract_text_from_pdf(file_path)
        if pdf_text:
            edited_file_stream = await analyze_and_edit_cv(
                update, context, template_choice,
                language_choice, pdf_text
            )
            new_file_name = f"edited_{user_file_name.rsplit('.', 1)[0]}.docx"
            logger.info(f"PDF file edited: {new_file_name}")
    else:
        await update.message.reply_text(Reply.WRONG_EXT.value)
        os.remove(file_path)
        logger.warning(f"Unsupported file type: {document.mime_type}")
        return

    if edited_file_stream:
        if isinstance(edited_file_stream, str):  # Если вернулся путь к файлу
            logger.error(f"Ошибка при обработке файла: {edited_file_stream[:20]}")
            await update.message.reply_text(Reply.BAD_RESPONSE.value)
            os.remove(file_path)
            return

        elif isinstance(edited_file_stream, io.BytesIO):  # Если уже BytesIO, проверяем, не пустой ли он
            if edited_file_stream.getbuffer().nbytes == 0:
                logger.error("Ошибка: файл пуст.")
                await update.message.reply_text(Reply.BAD_RESPONSE.value)
                os.remove(file_path)
                return

        logger.info(f"Отправляем файл {new_file_name} пользователю.")

        await update.message.reply_document(
            document=edited_file_stream,
            filename=new_file_name,
            caption=Reply.SUCCESS.value
        )
        logger.info("Edited file sent to user.")
    else:
        await update.message.reply_text(Reply.COMPATIBLE.value)
        logger.warning("File could not be edited.")


    os.remove(file_path)
    logger.info(f"Temporary file {file_path} removed.")
