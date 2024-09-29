import os

MODEL_API_BASE_URL = os.environ.get("MODEL_API_BASE_URL")

if not MODEL_API_BASE_URL:
    raise ValueError(
        "Не был указан URL для API модели, которая будет использована для получения ответов на пользовательские запросы"
    )

FETCH_PREDICTIONS_URL = MODEL_API_BASE_URL + "/predict"
