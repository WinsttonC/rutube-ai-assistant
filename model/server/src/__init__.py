from models import PredictRequest, PredictResponse
from utils import get_answer


async def predict(request: PredictRequest) -> PredictResponse:
    answer = get_answer(request.question)
    return PredictResponse(**answer)
