# Formats:
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Messages:
START_MESSAGE = (
    'Привет, {first_name}! Я бот, отвечающий за различные операции с CV. \n\n'
    'Для получения списка доступных команд введи /help \n\n'
    'Выбери команду: \n\n'
    '1. - Отредактировать CV по шаблону. \n'
    '2. - NA \n'
    '3. - NA \n'
    '4. - NA \n'
    '5. - NA \n'
    '6. - NA'
)
HELP_MESSAGE = (
    "📋 <b>Помощь по бот-командам</b>\n\n"
    "Вот что я умею:\n\n"
    "1️⃣ <b><u>Отредактировать CV:</u></b>\n\n"
    "Позволяет загружать CV кандидата в формате `.docx` или '.pdf', "
    "анализировать его и приводить к одному из выбранных шаблонов:\n\n"
    "- <b>Businessmatika</b>\n"
    "- <b>Huntercore</b>\n"
    "- <b>Telescope</b>\n\n"
    "Для использования выберите эту функцию в стартовом меню, "
    "определите требуемый шаблон CV и загрузите файл для редактирования.\n\n"
    "2️⃣ <b><u>Другие опции:</u></b>\n\n"
    "Пока не реализовано.\n\n"
    "<b><u>Команды:</u></b>\n\n"
    "/start - Запустить бота и выбрать действие.\n"
    "/help - Показать это меню помощи.\n"
    "/stop - Остановить бота.\n\n"
    "💡 По вопросам и пожеланиям пиши в телеграме @Ayreon2084."
)
STOP_MESSAGE = (
    'Ты остановил работу бота. Для возобновления работы нажми /start.'
)

# Docx:
DOCX_MIME_TYPE = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
PDF_MIME_TYPE = 'application/pdf'
