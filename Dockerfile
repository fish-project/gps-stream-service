FROM python:3.13.1-slim

WORKDIR /app

COPY . .

RUN python -m venv venv \
    && . venv/bin/activate \
    && pip install --no-cache-dir -r req.txt

COPY . .

CMD ["sh", "-c", ". venv/bin/activate && python -m src.run"]
