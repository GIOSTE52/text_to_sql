FROM python:3.12-slim

WORKDIR /backend

RUN apt-get update && apt-get install -y \
    mariadb-client \
    libmariadb-dev \
    gcc \
    curl \
    && apt-get clean

COPY . /backend
COPY ./data /backend/data

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8003

# CMD ["uvicorn", "src.serverAPI:app", "--host", "0.0.0.0", "--port", "8003", "--reload"]
CMD ["sh","-c", "python -m src.initialize_db && uvicorn src.serverAPI:app --host 0.0.0.0 --port 8003 --reload"]