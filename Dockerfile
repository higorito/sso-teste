FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir fastapi uvicorn python-dotenv requests

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
