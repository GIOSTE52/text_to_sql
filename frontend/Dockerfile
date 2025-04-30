FROM python:3.12-slim

WORKDIR /frontend

COPY . /frontend

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "src.serverHTML:app", "--host", "0.0.0.0", "--port", "8000"]