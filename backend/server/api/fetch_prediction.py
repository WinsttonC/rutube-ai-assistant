import httpx
import const
from models import PredictResponse, PredictRequest


async def fetch_prediction(question: PredictRequest) -> PredictResponse:
    """Функция для отправки HTTP-запроса на сервер с моделью для получения ответа на вопрос пользователя.

    Args:
        question (str): вопрос пользователя.

    Returns:
        _type_: _description_
    """
    async with httpx.AsyncClient():
        result = httpx.post(const.FETCH_PREDICTIONS_URL, json=question.model_dump())
        result = PredictResponse(**result.json())
    return result
