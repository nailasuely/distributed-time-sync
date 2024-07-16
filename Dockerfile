FROM python:3.9-slim

WORKDIR /app

COPY main.py .
COPY drift.py .
COPY vector_clock.py .

CMD ["python", "main.py"]