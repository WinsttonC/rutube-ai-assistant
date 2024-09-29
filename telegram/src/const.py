import os

BACKEND_BASE_URL = os.environ.get("BACKEND_BASE_URL")

if not BACKEND_BASE_URL:
    raise ValueError("Не был указан URL для бэкенд-сервиса телеграм-бота")

FETCH_PREDICTIONS_URL = BACKEND_BASE_URL + "/predict"

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Не был указан токен для телеграм-бота")
