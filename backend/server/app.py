from fastapi import FastAPI
from api.fetch_prediction import fetch_prediction
from models import PredictRequest, PredictResponse, TestResponse, IndexResponse

app = FastAPI()


@app.get("/test")
def test() -> TestResponse:
    response = {"response": "OK"}
    return TestResponse(**response)


@app.get("/")
def index() -> IndexResponse:
    response = {"text": "Интеллектуальный помощник оператора службы поддержки."}
    return IndexResponse(**response)


@app.post("/predict")
async def predict_sentiment(request: PredictRequest) -> PredictResponse:
    result = await fetch_prediction(request)
    return result
