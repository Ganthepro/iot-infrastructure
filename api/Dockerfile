FROM python:3.11-slim

RUN apt update && apt install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./api .
EXPOSE 8000

CMD ["fastapi", "run"]