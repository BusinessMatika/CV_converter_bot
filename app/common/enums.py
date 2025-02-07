import json
from enum import Enum

from docx.shared import RGBColor


class Button(Enum):
    BACK = '⬅️ Назад'
    BUSINESSMARIKA = 'Businessmatika'
    CV_EVALUATION = '2️⃣ Оценить CV для вакансии (НАХОДИТСЯ В РАЗРАБОТКЕ!)'
    EDIT_CV = '1️⃣ Отредактировать CV'
    ENGLISH = 'Английский'
    FILE = 'Файл'
    HUNTERCORE = 'Huntercore'
    RUSSIAN = 'Русский'
    STOP = '❌ Остановить работу'
    TELESCOPE = 'Telescope'
    TEXT = 'Текст'


class Callback(Enum):
    BUSINESSMATIKA = 'businessmatika'
    CV_EVALUATION = 'cv_evaluation'
    EDIT_CV = 'edit_cv'
    ENGLISH = 'english'
    FILE = 'file'
    HUNTERCORE = 'huntercore'
    RETURN_TO_START = 'return_to_start'
    RUSSIAN = 'russian'
    STOP_BOT = 'stop_bot'
    TELESCOPE = 'telescope'
    TEXT = 'text'


class CVTemplate(Enum):
    BUSINESSMATIKA = 'businessmatika'
    HUNTERCORE = 'huntercore'
    TELESCOPE = 'telescope'


class CVTranslation(Enum):
    ENGLISH = 'Английский'
    RUSSIAN = 'Русский'


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
    CODE = ('Примеры кода: ', 'Code examples: ')
    COURSES = 'courses'
    DATES = 'dates'
    DESCR = ('\nО себе: ', '\nAbout: ')
    EDUCATION = 'education'
    EXP = 'experience'
    FULL_NAME = 'full_name'
    GRADE_TITLE = ('Грейд: ', 'Grade: ')
    GRADE_DATA = 'grade'
    HEADER = 'header'
    ITEMS = 'items'
    JOB_TITLE = 'job_title'
    LANGUAGES = 'languages'
    PROJECT = [
        ('Название проекта: ', 'project_name', True),
        ('Описание проекта: ', 'project_description', False),
    ], [
        ('Project name: ', 'project_name', True),
        ('Project description: ', 'project_description', False),
    ]
    REPO = 'repository'
    ROLE = 'role'
    SECTIONS = 'sections'
    SKILLS = 'skills'
    TASKS_ACHIEVEMENTS = [
        ('Задачи:', 'tasks'),
        ('Достижения:', 'achievements')
    ], [
        ('Tasks:', 'tasks'),
        ('Achievements:', 'achievements')
    ]
    TEAM_STACK = [
        ('Команда: ', 'team'),
        ('Стек: ', 'stack')
    ], [
        ('Team: ', 'team'),
        ('Stack: ', 'stack')
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
    HUNT_HEADER_H = 0.92
    HUNT_HEADER_WD = 4.76
    TEL_HEADER_H = 0.92
    TEL_HEADER_WD = 4.76
    NINE = 9
    TEN = 10
    TWENTY = 20

    # Other
    BULLET = 'List Bullet'


class OpenAI(Enum):
    MODEL = 'gpt-3.5-turbo'
    JSON_RUS = {
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
    PROMPT_RUS = (
        "Твоя задача — проанализировать резюме, заполнить JSON-шаблон, перевести JSON-шаблон на русский язык.\n\n"
        "Правила:\n"
        "1. Строго следуй JSON-шаблону (не добавляй новые поля, не меняй названия секций).\n"
        "2. Разделяй списки корректно: \n"
        "   - 'tasks' — это **конкретные действия** (например, 'Разработал API').\n"
        "   - 'project_description' — это **описание проекта** (например, 'Финансовый стартап').\n\n"
        "3. Если информация отсутствует, заполняй поле пустой строкой, но **не удаляй его**.\n"
        "4. Выводи только JSON без лишнего текста.\n\n"
        "Данные:\n"
        "JSON-шаблон: {json_str}\n"
        "Резюме пользователя:\n{user_content}\n\n"
        "Теперь обработай резюме и выведи корректный JSON, полностью переведённый на русский язык."
    )
    JSON_ENG = {
        "header": {
            "full_name": "<Full name>",
            "job_title": "<Job title>",
            "grade": "<Junior | Junior+ | Middle | Middle+ | Senior | Team Lead>",
            "repository": "<Repository link> (e.g. github.com/@example etc)",
            "about": "<About yourself, self-presentation (do not include technologies from other sections)>"
        },
        "sections": {
            "languages": {
                "title": "Languages:",
                "items": [
                    "<Language - proficiency level>"
                ]
            },
            "skills": {
                "title": "Skills:",
                "items": [
                    "<Skills>"
                ]
            },
            "experience": {
                "title": "Work experience:",
                "items": [
                    {
                        "role": "<Role, job title>",
                        "dates": "<Month year - month year>",
                        "project_name": "<Project, company name>",
                        "project_description": "<Project description>",
                        "tasks": [
                            "<Task>"
                        ],
                        "achievements": [
                            "<Achievement>"
                        ],
                        "team": "<Team size, participants>",
                        "stack": "<Technology>"
                    }
                ]
            },
            "education": {
                "title": "Education:",
                "items": [
                    "<Year of graduation | Educational institution, specialization> (e.g. 2012 | Moscow State University, Faculty of Journalism)"
                ]
            },
            "courses": {
                "title": "Courses, additional training:",
                "items": [
                    "<Year of completion | Educational institution, specialization> (e.g 2014 | Stepik, Fullstack Developer course)"
                ]
            }
        }
    }
    PROMPT_ENG = (
        "Your task is to analyze the resume and strictly fill in JSON template.\n\n"
        "Rules:\n"
        "1. Strictly follow the JSON structure (do not add or rename fields).\n"
        "2. Separate list elements correctly:\n"
        '   - "tasks" = Specific actions (e.g., "Developed an API").\n'
        '   - "stack" = Specific technologies, programming languages (e.g., "Python").\n'
        '   - "project_description" = General project description (e.g., "A fintech startup").\n\n'
        "3. If a section is missing, return an empty string but keep the JSON structure.\n"
        "4. Output only the JSON without extra text.\n\n"
        "Input data:\n"
        "JSON template: {json_str}\n"
        "Resume text:\n{user_content}\n\n"
        "Now process the resume and return the JSON fully translated in English language."
    )

    @staticmethod
    def get_messages(user_content: str, json_str: str, prompt_choice: str) -> list[dict]:
        json_str = json.dumps(json_str, ensure_ascii=False, indent=4)
        if prompt_choice == 'russian':
            prompt = OpenAI.PROMPT_RUS.value
        elif prompt_choice == 'english':
            prompt = OpenAI.PROMPT_ENG.value
        else:
            raise ValueError(f"Invalid prompt choice: {prompt_choice}")
        return [
            {
                'role': 'system',
                'content': 'You are a professional JSON template generator.'
            },
            {
                'role': 'user',
                'content': prompt.format(
                    user_content=user_content,
                    json_str=json_str
                )
            }
        ]


class Reply(Enum):
    BAD_RESPONSE = (
        'Не получилось обработать файл.\n'
        'Возможно файл повреждён или содержит слишком сложную структуру.\n'
        'Если файл был в формате .docx, попробуйте преобразовать его в .pdf и отправить повторно.\n\n'
        'В случае очередной неудачи это означает, что на текущей итерации функционала бота '
        'обеспечить чтение и редактирование файла невозможно.\n\n'
    )
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
        'преобразован в шаблон <b>"{template_name}"</b> на <b>{language_name}</b> языке.\n\n'
        'Дождитесь загрузки файла.'
    )
    NOT_EXIST = 'Опция <b>"{query}"</b> пока недоступна.'
    SUCCESS = (
        'Вот ваш обновлённый файл с CV!\n\n'
        'В случае неудовлетворительного результата можете отправить CV для повторного редактирования.'
    )
    TEMPLATE_CHOICE = (
        'Вы выбрали шаблон <b>"{template}"</b>.\n\n'
        'Выберите язык перевода CV.'
    )
    TRANSLATION_CHOICE = (
        'Вы выбрали <b>"{language}"</b> язык.\n\n'
        'Загрузите CV в формате .docx или .pdf, чтобы отредактировать его.'
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
