FROM python:3.11-slim

RUN python3 -m fastchat.serve.controller \
    python3 -m fastchat.serve.model_worker --model-name openchat/openchat-3.6-8b-20240522 \
    python3 -m fastchat.serve.openai_api_server --host 0.0.0.0 --port 8000

COPY requirements.txt /app
RUN pip install -r /app/requirements.txt

COPY server/ /app/src/
EXPOSE 8000
WORKDIR /app/src/
RUN python3 create_vectorstore.py

ENTRYPOINT uvicorn --workers 8 --host 0.0.0.0 --port 80 app:app