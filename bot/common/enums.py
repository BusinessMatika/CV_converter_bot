from enum import Enum


class Button(Enum):
    BACK = 'Назад'
    EVIT_CV = '1️⃣ Отредактировать CV'
    STOP = '❌ Остановить работу'

class Callback(Enum):
    EDIT_CV = 'edit_cv'
    RETURN_TO_START = 'return_to_start'
    STOP_BOT = 'stop_bot'


class Handler(Enum):
    HELP = 'help'
    START = 'start'
    STOP = 'stop'


class OpenAI(Enum):
    MODEL = 'gpt-3.5-turbo'
    PROMPT = (
        "You are a document conversion assistant. Your task is to take a user-provided document, which "
        "can have any format, structure, or content, and transform it into a document that fully matches "
        "the structure, formatting, and style of the provided reference document. "
        "Always produce an updated document, even if the input is incomplete or poorly formatted. "
        "Do not return errors or comments like 'the formats are different'. Instead, make your best effort "
        "to transform the user's document into the reference format. If the content is unclear, you may infer "
        "reasonable placeholders. Here are the documents:\n\n"
        "User Document:\n{user_content}\n\n"
        "Reference Document:\n{reference_content}\n\n"
        "Please provide the transformed document below in plain text format:"
    )

    @staticmethod
    def get_messages(user_content: str, reference_content: str) -> list[dict]:
        return [
            {'role': 'system', 'content': 'You are an assistant that ensures document compatibility.'},
            {'role': 'user', 'content': OpenAI.PROMPT.value.format(
                user_content=user_content,
                reference_content=reference_content
            )}
        ]


class Reply(Enum):
    COMPATIBLE = 'Ваш файл уже совместим с референсом.'
    EDIT_CV = (
        'Вы выбрали: Отредактировать CV. '
        'Загрузите CV в формате .docx, чтобы отредактировать его.'
    )
    NOT_EXIST = 'Опция {query} пока недоступна.'
    SUCCESS = 'Вот ваш обновлённый файл с CV!'
    WRONG_EXT = 'Вы отправили файл не с тем расширением. Прошу отправить .docx'
