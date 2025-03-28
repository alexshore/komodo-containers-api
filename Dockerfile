FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir fastapi[all] httpx

EXPOSE 9121

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9121"]