FROM python:3.11-slim

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1
#RUN curl -sSL https://install.python-poetry.org | python3 -
RUN pip install poetry
COPY poetry.lock pyproject.toml .
RUN poetry install --no-interaction --no-ansi
COPY src/ src/
EXPOSE 8000
WORKDIR src/
#ENTRYPOINT gunicorn --reload -w 4 -b 0.0.0.0:8000 'app:app'
ENTRYPOINT uvicorn --workers 8 --host 0.0.0.0 --port 80 app:app