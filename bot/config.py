import os
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
BOT_FOLDER = 'bot'
REF_CV_FOLDER = 'reference_cv'
REF_CV_FILE = 'reference_cv.docx'
REFERENCE_CV = BASE_DIR / BOT_FOLDER / REF_CV_FOLDER / REF_CV_FILE
EDITED_CV = f'edited_{uuid4()}.docx'

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
