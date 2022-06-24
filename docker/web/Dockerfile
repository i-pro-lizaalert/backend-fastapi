FROM python:3.10-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD python -m uvicorn app.api:app --host 0.0.0.0 --port ${SERVER_PORT}
