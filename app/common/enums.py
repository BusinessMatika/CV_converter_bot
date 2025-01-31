import json
from enum import Enum

from docx.shared import RGBColor


class Button(Enum):
    BACK = '⬅️ Назад'
    BUSINESSMARIKA = 'Businessmatika'
    CV_EVALUATION = '2️⃣ Оценить CV для вакансии (НАХОДИТСЯ В РАЗРАБОТКЕ!)'
    EDIT_CV = '1️⃣ Отредактировать CV'
    FILE = 'Файл'
    HUNTERCORE = 'Huntercore'
    STOP = '❌ Остановить работу'
    TELESCOPE = 'Telescope'
    TEXT = 'Текст'


class Callback(Enum):
    BUSINESSMATIKA = 'businessmatika'
    CV_EVALUATION = 'cv_evaluation'
    EDIT_CV = 'edit_cv'
    FILE = 'file'
    HUNTERCORE = 'huntercore'
    RETURN_TO_START = 'return_to_start'
    STOP_BOT = 'stop_bot'
    TELESCOPE = 'telescope'
    TEXT = 'text'


class CVTemplate(Enum):
    BUSINESSMATIKA = 'businessmatika'
    HUNTERCORE = 'huntercore'
    TELESCOPE = 'telescope'


class Handler(Enum):
    HELP = 'help'
    START = 'start'
    STOP = 'stop'

class Table(Enum):
    # Borders
    BM_BOTTOM = '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="E14919"/>'
    BM_TOP = '<w:top w:val="single" w:sz="8" w:space="0" w:color="E14919"/>'
    HUNTERCORE_BOTTOM = '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="00ffff"/>'
    HUNTERCORE_TOP = '<w:top w:val="single" w:sz="8" w:space="0" w:color="00ffff"/>'
    TELESCOPE_BOTTOM = '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="a8caf8"/>'
    TELESCOPE_TOP = '<w:top w:val="single" w:sz="8" w:space="0" w:color="a8caf8"/>'
    TRANSCEND = '<w:top w:val="nil" w:sz="0" w:space="0" w:color="auto"/>'
    STYLE = 'Table Grid'
    # Dimensions
    ROWS = 0
    COLS = 2
    MAX_COLS = 3


class JSONData(Enum):
    ABOUT = 'about'
    CODE = 'Примеры кода: '
    COURSES = 'courses'
    DATES = 'dates'
    DESCR = '\nО себе: '
    EDUCATION = 'education'
    EXP = 'experience'
    FULL_NAME = 'full_name'
    GRADE_TITLE = 'Грейд: '
    GRADE_DATA = 'grade'
    HEADER = 'header'
    ITEMS = 'items'
    JOB_TITLE = 'job_title'
    LANGUAGES = 'languages'
    PROJECT = [
        ('Название проекта: ', 'project_name', True),
        ('Описание проекта: ', 'project_description', False),
    ]
    REPO = 'repository'
    ROLE = 'role'
    SECTIONS = 'sections'
    SKILLS = 'skills'
    TASKS_ACHIEVEMENTS = [
        ('Задачи:', 'tasks'),
        ('Достижения:', 'achievements')
    ]
    TEAM_STACK = [
        ('Команда: ', 'team'),
        ('Стек: ', 'stack')
    ]
    TITLE = 'title'


class Number(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2


class Style(Enum):
    # Colors
    BLACK = RGBColor(0, 0, 0)
    GREY = RGBColor(89, 89, 89)
    HEX_GREY = '#595959'
    # Fonts
    RALEWAY = 'Raleway'
    RALEWAY_LIGHT = 'Raleway Light'
    RALEWAY_MEDIUM = 'Raleway Medium'
    AVAILABLE_FONTS = (RALEWAY, RALEWAY_LIGHT, RALEWAY_MEDIUM)
    # Size
    BM_FOOTER_H = 1.09
    BM_FOOTER_WD = 3.56
    BM_HEADER_H = 0.92
    BM_HEADER_WD = 4.76
    HUNT_HEADER_H = 0.92 #1.28
    HUNT_HEADER_WD = 4.76 #6.56
    TEL_HEADER_H = 0.92 #0.97
    TEL_HEADER_WD = 4.76 #4.52
    NINE = 9
    TEN = 10
    TWENTY = 20

    # Other
    BULLET = 'List Bullet'


class OpenAI(Enum):
    MODEL = 'gpt-3.5-turbo'
    JSON = {
        "header": {
            "full_name": "<Имя, фамилия, отчество>",
            "job_title": "<Должность>",
            "grade": "<Junior | Junior+ | Middle | Middle+ | Senior | Team Lead>",
            "repository": "<Ссылка на репозиторий> (e.g. github.com/@example etc)",
            "about": "<Информация о себе, самопрезентация (не включай сюда технологии из других разделов)>"
        },
        "sections": {
            "languages": {
                "title": "Языки:",
                "items": [
                    "<Язык - уровень владения>"
                ]
            },
            "skills": {
                "title": "Навыки:",
                "items": [
                    "<Навыки>"
                ]
            },
            "experience": {
                "title": "Опыт работы:",
                "items": [
                    {
                        "role": "<Роль, должность>",
                        "dates": "<Месяц год - месяц год>",
                        "project_name": "<Название проекта, компании>",
                        "project_description": "<Описание проекта>",
                        "tasks": [
                            "<Задача>"
                        ],
                        "achievements": [
                            "<Достижение>"
                        ],
                        "team": "<Размер команды, участники>",
                        "stack": "<Технология>"
                    }
                ]
            },
            "education": {
                "title": "Образование:",
                "items": [
                    "<Год окончания | Учебное заведение, специализация> (e.g. 2012 | МГУ, Факультет журналистики)"
                ]
            },
            "courses": {
                "title": "Курсы, дополнительное обучение:",
                "items": [
                    "<Год окончания | Учебное заведение, специализация> (e.g 2014 | Stepik, Fullstack Developer course)"
                ]
            }
        }
    }
    PROMPT = (
        "Your task is to extract the data from the provided CV and populate the JSON template accordingly. "
        "Follow these rules: "
        "1. Fill all fields under 'header' and 'sections' with the corresponding information from the CV. "
        "2. Use lists (arrays) for fields such as 'languages', 'skills', 'tasks', 'achievements', and others that may contain multiple entries. "
        "3. For fields such as 'text', extract the corresponding value directly from the CV. "
        "4. Ensure all data in the resulting JSON is correctly filled and matches the structure provided in the template. "
        "5. If a section is empty or does not apply, leave it as an empty string, but maintain the structure.\n "
        "6. Do not apply any creativity.\n"
        "7. If 'tasks' in CV has text line instead of lists with text, put this info in 'project_description' value"
        "Input Data: \n"
        "JSON: {json_str}\n"
        "USER_CV: {user_content}\n\n"
        "Now process the USER_CV and return the populated JSON."
    )

    @staticmethod
    def get_messages(user_content: str, json_str: str) -> list[dict]:
        json_str = json.dumps(json_str, ensure_ascii=False, indent=4)
        return [
            {
                'role': 'system',
                'content': 'You are a professional JSON template generator.'
            },
            {
                'role': 'user',
                'content': OpenAI.PROMPT.value.format(
                    user_content=user_content,
                    json_str=json_str
                )
            }
        ]


class Reply(Enum):
    COMPATIBLE = 'Ваш файл уже совместим с референсом.'
    CV_EVALUATION = (
        'Вы выбрали: <b>"Оценить CV для вакансии"</b>.\n\n'
        'Выберите вариант отправки описания вакансии: '
        'текстом или файлом в форматах .docx или .pdf'
    )
    EDIT_CV = (
        'Вы выбрали: <b>"Отредактировать CV"</b>.\n\n'
        'Теперь выберете необходимый шаблон для CV.'
    )
    EDIT_CV_EXECUTION = (
        'Файл <b>"{file_name}"</b> успешно загружен и будет '
        'преобразован в шаблон <b>"{template_name}"</b>.\n\n'
        'Дождитесь загрузки файла.'
    )
    NOT_EXIST = 'Опция <b>"{query}"</b> пока недоступна.'
    SUCCESS = 'Вот ваш обновлённый файл с CV!'
    TEMPLATE_CHOICE = (
        'Вы выбрали шаблон <b>"{template}"</b>.\n\n'
        'Загрузите CV в формате .docx или .pdf, чтобы отредактировать его.\n\n'
        'Если полученный результат будет неудовлетворительным (такое случается, увы), '
        'отправьте файл заново.'
    )
    VACANCY_FILE = (
        'Вы выбрали <b>"Текст"</b>. '
        'Отправьте в чат текст с описанием вакансии. '
    )
    VACANCY_TEXT = (
        'Вы выбрали <b>"Файл"</b>.\n\n'
        'Загрузите описание вакансии в формате .docx или .pdf. '
    )
    WRONG_EXT = 'Вы отправили файл не с тем расширением. Прошу отправить .docx или .pdf'
