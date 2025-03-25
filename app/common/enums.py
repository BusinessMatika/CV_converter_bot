import json
from enum import Enum
from typing import Optional

from docx.shared import RGBColor

from app.config import logger


class Button(Enum):
    BACK = '⬅️ Назад'
    BUSINESSMARIKA = 'Businessmatika'
    CV_EVALUATION = '2️⃣ Сравнить CV кандидата с вакансией'
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
    MANAGE_USERS = 'manage_users'


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
    """Common configuration of OpenAI"""
    MODEL_3_5_TURBO = 'gpt-3.5-turbo'
    MODEL_4_TURBO = 'gpt-4-turbo'
    MODEL_4 = 'gpt-4'


class EditCV(Enum):
    """Enums for Edit CV command"""
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
            prompt = EditCV.PROMPT_RUS.value
        elif prompt_choice == 'english':
            prompt = EditCV.PROMPT_ENG.value
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


class EvaluateVacancyCV(Enum):
    eval_vac_prompt = (
        "You are an expert HR professional specializing in job vacancy analysis."
        "Your role is to extract and summarize the most important requirements and details from a single job description per request,"
        "ensuring it can be easily compared with a candidate’s CV later. Your analysis should focus only on major details to streamline the comparison process. \n\n"

        "When analyzing a vacancy, you should extract and return the following information in JSON format:\n"

        '- "Job Title"\n'
        '- "Location"\n'
        '- "Experience Level" (Entry, Mid, Senior, etc.)\n'
        '- "Responsibilities" (as an array)\n'
        '- "Requirements" (as an array)\n'
        '- "Preferred Qualifications" (as an array, if mentioned)\n'

        "Your response must always be in valid JSON format to ensure easy analysis."
        'If any critical details are missing from the vacancy description, return an empty string ("") or an empty array ("[]") instead of assuming values. \n'

        "Always maintain a professional and neutral tone."

        "Vacancy:\n\n{vacancy_data}"
    )

    eval_vac_cv_prompt = (
        """
        You are a professional HR recruiter responsible for evaluating candidates based on job vacancies provided by clients. The client will send a JSON file containing job details with fixed keys, but varying values. Alongside the vacancy details, a candidate's CV will also be provided.

        Your task is to assess each candidate against the given vacancy. For vacancies with list-type data (such as responsibilities and requirements), each individual element should be evaluated separately. Each criterion should be highlighted for readability.

        Evaluation criteria:
        - Assign a score from 0 to 5 for each point in the job description:
        - 0: ❌ (Not match at all)
        - 1-5: ⭐ (Stars based on relevance, e.g., ⭐⭐⭐⭐ for a 4/5 match)
        - Provide a brief explanation for each score.

        Additional considerations when analyzing work experience:
        1) Identify long gaps in work experience and highlight any recent periods of unemployment.
        2) Evaluate job stability: frequent job changes are a red flag and should be noted.
        3) Assess only relevant work experience. If a candidate has 20 years of total experience but only 2 years in the required role, count only those 2 years.
        4) Examine work experience and tasks performed.  If tasks and achievements are repeated multiple times across the CV without added value, highlight this as a potential issue.
        5) Prioritize experience in well-known, reputable companies over unknown or small organizations.
        6) Verify hard skills. Ensure that skills listed in the CV are also reflected in the candidate’s work experience. If a skill is mentioned but not supported by work history, highlight it as unproven.

        At the end of the evaluation:
        - Calculate the candidate's overall compatibility percentage (0-100%) and explain your decision.
        - Summarize the strengths and weaknesses of the candidate based on the assessment.
        - Evaluate experience level.
        - Highlight the best characteristics of the candidate.
        - Highlight the weakest aspects that do not align with the vacancy.
        - Provide recommendations for improving the candidate's CV to better match the job requirements.
        - Explicitly highlight any red flags in the response (e.g., job gaps, frequent changes, lack of proven hard skills, excessive repetition of tasks, etc.), ensuring that the recruiter is alerted to these issues for manual review or candidate follow-up.
        - Include a final <b>concise recommendation</b> on whether this candidate should be sent to the client or not.

        The final result should be highlighted using only the following tags: <b>bold</b>, <i>italic</i>, <u>underline</u> for readability. Avoid Markdown formatting and any other HTML tags.

        All results should be provided in Russian.
        Vacancy_data:\n
        {vacancy_data}\n\n

        CV data:\n
        {cv_data}
        """
    )

    @staticmethod
    def get_messages(prompt_choice: str, vacancy_data: str, cv_data: Optional[str] = None) -> list[dict]:
        cv_data = f'📌 <b>Резюме кандидата:(для анализа)</b>\n{cv_data}\n\n' if cv_data else ''

        return [
            {
                'role': 'system',
                'content': 'You are an HR expert in job vacancy description analysis and CV compatibility to this vacancy. '
            },
            {
                'role': 'user',
                'content': prompt_choice.format(
                    vacancy_data=vacancy_data,
                    cv_data=cv_data,
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
    FILE_NOT_FOUND = (
        'Вам требуется или выбрать команду, или отправить файл согласно инструкции.'
    )
    COMPATIBLE = 'Ваш файл уже совместим с референсом.'
    CV_EVALUATION = (
        'Вы выбрали: <b>"Оценить CV для вакансии"</b>.\n\n'
        'Отправьте описание вакансии одним из следующих споcобов:\n\n'
        '- текстовым сообщением в чат;\n'
        '- файлом в формате .docx или .pdf'
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
    VACANCY_EVAL_EXECUTION = (
        'Файл с вакансией <b>"{file_name}"</b> успешно загружен и будет '
        'проанализирован с целью дальнейшего сопоставления с CV.\n\n'
        'Дождитесь загрузки файла.'
    )
    VACANCY_CV_EVAL_EXECUTION = (
        'Файл с CV <b>"{file_name}"</b> успешно загружен и будет '
        'проанализирован совместно с ранее загруженной вакансией с целью дальнейшего сопоставления и оценки.\n\n'
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
    EVALUATE_VACANCY = (
        'EVALUATE_VACANCY'
    )
    EVALUATE_CV = (
        'EVALUATE_CV'
    )
    WRONG_EXT = 'Вы отправили файл не с тем расширением. Прошу отправить .docx или .pdf'
