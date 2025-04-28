from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response
import requests

app = FastAPI(title = "text_to_sql Server HTML")
templates = Jinja2Templates(directory= "frontend/templates")

API_BASE_URL = "http://localhost:8003"

@app.get("/")
def root(request : Request):
    try:
        response = requests.get(f"{API_BASE_URL}/")
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        data = {"errore" : f"Errore durante la chiamata al server: {e}"}
    return templates.TemplateResponse("index.html", {"request":request, "data" : data})


@app.get("/schema_summary")
def get_schema_summary(request : Request):

    return templates.TemplateResponse("index.html")