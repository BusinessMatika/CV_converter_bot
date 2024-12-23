import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('DEBUG') == 'True'

BASE_DIR = Path(__file__).resolve().parent.parent

# Bot:
BOT_FOLDER = 'bot'

# Static:
STATIC_FOLDER = 'static'
HEADER_FILE = 'header.png'
FOOTER_FILE = 'footer.png'
HEADER_PATH = str(BASE_DIR / BOT_FOLDER / STATIC_FOLDER / HEADER_FILE)
FOOTER_PATH = str(BASE_DIR / BOT_FOLDER / STATIC_FOLDER / FOOTER_FILE)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
