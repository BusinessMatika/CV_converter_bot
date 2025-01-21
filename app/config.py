import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from app.common.constants import LOG_FORMAT

load_dotenv()

DEBUG = os.getenv('DEBUG') == 'True'

BASE_DIR = Path(__file__).resolve().parent.parent

# Bot:
BOT_FOLDER = 'app'

# Static:
STATIC_FOLDER = 'static'
BM_HEADER_FILE = 'bm_header.png'
BM_FOOTER_FILE = 'bm_footer.png'
HUNTERCORE_HEADER_FILE = 'huntercore_header.png'
TELESCOPE_HEADER_FILE = 'telescope_header.png'
BM_HEADER_PATH = str(BASE_DIR / BOT_FOLDER / STATIC_FOLDER / BM_HEADER_FILE)
BM_FOOTER_PATH = str(BASE_DIR / BOT_FOLDER / STATIC_FOLDER / BM_FOOTER_FILE)
HUNTERCORE_HEADER_PATH = str(
    BASE_DIR / BOT_FOLDER / STATIC_FOLDER / HUNTERCORE_HEADER_FILE
)
TELESCOPE_HEADER_PATH = str(
    BASE_DIR / BOT_FOLDER / STATIC_FOLDER / TELESCOPE_HEADER_FILE
)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Logger:
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
