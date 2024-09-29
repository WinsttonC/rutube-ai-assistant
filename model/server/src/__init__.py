from models import PredictRequest, PredictResponse


async def predict(request: PredictRequest) -> PredictResponse:
    return PredictResponse(**{})
