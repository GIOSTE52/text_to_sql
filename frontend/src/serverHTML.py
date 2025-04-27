from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response
import requests

app = FastAPI(title = "text_to_sql Server HTML")
templates = Jinja2Templates(directory= "../templates")

API_BASE_URL = "http://localhost:8003"

@app.get("/")
def root(request : Request):
    return templates.TemplateResponse("index.html", {"request":request})
