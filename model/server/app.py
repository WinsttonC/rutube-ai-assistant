from fastapi import FastAPI
from src import predict
from models import PredictRequest, PredictResponse, TestResponse

app = FastAPI()


@app.get("/test")
def test() -> TestResponse:
    response = {"response": "OK"}
    return TestResponse(**response)


@app.post("/predict")
async def predict_sentiment(request: PredictRequest) -> PredictResponse:
    result = PredictResponse(answer="hello", class_1="a", class_2="b")  # result = await predict(request)
    return result
