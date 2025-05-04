from fastapi import FastAPI, HTTPException, Request, Form, Body
from fastapi.templating import Jinja2Templates
import requests
from pydantic import BaseModel

class AddPayload(BaseModel):
    data_line : str

app = FastAPI(title = "text_to_sql Server HTML")
templates = Jinja2Templates(directory= "templates")

API_BASE_URL = "http://backend:8003"

@app.get("/")
def root(request : Request):
    try:
        response = requests.get(f"{API_BASE_URL}/")
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        data = {"errore" : f"Errore durante la chiamata GET \"/\": {e}"}
        # raise HTTPException(status_code=500, detail=f"Errore nella richiesta al server: {e}")
    return templates.TemplateResponse("index.html", {"request":request, "data" : data})


@app.get("/schema_summary")
def get_schema_summary(request : Request):
    try:
        response = requests.get(f"{API_BASE_URL}/schema_summary")
        response.raise_for_status()
        schema = response.json() 
    except requests.exceptions.RequestException as e:
        schema = {"errore" : f"Errore durante la chiamata GET \"/schema_summary\": {e}"}
        # raise HTTPException(status_code=500, detail=f"Errore nella richiesta al server: {e}")
    return templates.TemplateResponse("index.html", {"request":request, "schema": schema})

@app.get("/search")
def get_search(request : Request, query : str):
    try:
        response = requests.get(f"{API_BASE_URL}/search/{query}")
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as e:
        result = {"errore" : f"Errore durante la chiamata GET \"/search\": {e}"}
        # raise HTTPException(status_code=500, detail=f"Errore nella richiesta al server: {e}")
    return templates.TemplateResponse("index.html", {"request" : request, "result" : result})

@app.post("/add")
def post_add(request : Request, data_line : str = Form(...)):
    if not data_line:
        status = {"status" : f"Errore durante la chiamata POST \"/add\": {e}"}
        # raise HTTPException(status_code=422, detail=f"Errore dei tipi di dati: {e}") 
    try:
        response = requests.post(f"{API_BASE_URL}/add", json = {"data_line" : data_line})
        response.raise_for_status()
        status = response.json()
    except ValueError as e:
        status = {"errore" : f"Errore dati non validi: {e}"}
        # raise HTTPException(status_code=422, detail=f"Errore dei tipi di dati: {e}") 
    except requests.exceptions.RequestException as e:
        status = {"errore" : f"Errore durante la chiamata POST \"/add\": {e}"}
        # raise HTTPException(status_code=500, detail=f"Errore nella richiesta al server: {e}")
    return templates.TemplateResponse("index.html", {"request":request, "status" : status})

