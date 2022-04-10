FROM tiangolo/uvicorn-gunicorn-fastapi

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY alembic/ ./alembic
COPY alembic.ini prestart.sh ./
COPY ./app /app/app