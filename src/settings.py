import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
API_TOKEN = os.getenv("API_TOKEN")

SRC_DIR = Path(__file__).parent  # \your\home\directory\brontosaurus_process_mining\src
