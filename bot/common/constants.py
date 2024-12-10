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
    "📋 *Помощь по бот-командам*\n\n"
    "Вот что я умею:\n\n"
    "1️⃣ *Отредактировать CV*:\n"
    "   Позволяет загружать CV кандидата в формате `.docx`, анализировать его и приводить к заданному шаблону. "
    "Для использования выберите эту опцию через /start и загрузите файл.\n\n"
    "2️⃣ *Другие опции*: \n"
    "   Пока не реализовано.\n\n"
    "*Команды:*\n"
    "/start - Запустить бота и выбрать действие.\n"
    "/help - Показать это меню помощи.\n"
    "/stop - Остановить бота.\n"
    "💡 По вопросам и пожеланиям пиши в телеграме @Ayreon2084."
)
STOP_MESSAGE = (
    'Ты остановил работу бота. Для возобновления работы нажми /start.'
)

# Docx:
DOCX_MIME_TYPE = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

# EDIT_CV_PROMPT = "Upload a .docx file to edit your CV."
# BACK_BUTTON = [InlineKeyboardButton("Back", callback_data="return_to_start")]