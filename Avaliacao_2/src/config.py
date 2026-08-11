import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent


GMAIL_URL = os.getenv(
    "GMAIL_URL",
    "https://mail.google.com/"
)

GMAIL_LABEL = os.getenv(
    "GMAIL_LABEL",
    "CADASTROS/NOVOS"
)

DATA_DIR = BASE_DIR / os.getenv(
    "DATA_DIR",
    "data"
)

OUTPUT_DIR = BASE_DIR / os.getenv(
    "OUTPUT_DIR",
    "output"
)

BROWSER_PROFILE = BASE_DIR / os.getenv(
    "BROWSER_PROFILE",
    "browser/profile"
)

EXCEL_FILE = BASE_DIR / os.getenv(
    "EXCEL_FILE",
    "output/cadastros.xlsx"
)

OCR_ENABLED = (
    os.getenv("OCR_ENABLED", "true").lower() == "true"
)

OCR_LANGUAGE = os.getenv(
    "OCR_LANGUAGE",
    "por"
)

HEADLESS = (
    os.getenv("HEADLESS", "false").lower() == "true"
)


DOCUMENTS_OK = DATA_DIR / "documentos_ok"
DOCUMENTS_PENDING = DATA_DIR / "documentos_pendentes"
MANUAL_REVIEW = DATA_DIR / "revisao_manual"
ERROR_DIR = DATA_DIR / "erro"
PROCESSING_DIR = DATA_DIR / "processamento"


def create_directories():
    directories = [
        DATA_DIR,
        OUTPUT_DIR,
        BROWSER_PROFILE,
        DOCUMENTS_OK,
        DOCUMENTS_PENDING,
        MANUAL_REVIEW,
        ERROR_DIR,
        PROCESSING_DIR,
        EXCEL_FILE.parent,
    ]

    for directory in directories:
        directory.mkdir(
            parents=True,
            exist_ok=True
        )