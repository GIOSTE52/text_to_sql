from config.paths import DB_CONFIG
from utils.parse_data import *

from fastapi import FastAPI, HTTPException, requests
from pydantic import BaseModel
from typing import List
import mariadb
    
app = FastAPI(title="text_to_sql")

#Imposto il formato delle tabelle da restituire in output alla richiesta GET schema_summary
class TableSchema(BaseModel):
    table_name : str
    table_column : str
#Imposto il formato degli attributi e i loro valori
class PropertySchema(BaseModel):
    property_name : str
    property_value : str
#Imposto il formato dei risultati delle query SELECT
class SelectResponse(BaseModel):
    item_type : str
    properties : List[PropertySchema]
#Imposto il formato del risultato della richiesta GET "/search"
class SearchResponse(BaseModel):
    result : List[SelectResponse]

#Gestisco possibili errori durante la connessione al database
try:
    db_conn = mariadb.connect(**DB_CONFIG)
except mariadb.Error as e:
    print(f"Errore nella connessione al database: {e}")
    exit(1)
    
#Creo il cursore(punto di contatto) per gestire la connessione con il database
db_cursor : mariadb.Cursor = db_conn.cursor()

@app.get("/schema_summary")
def get_schema_summary()->None:

    result : List[TableSchema] = []
    table = TableSchema(
        
    )

@app.get("/search", response = SearchResponse)
def search(question : str):
    parsed = parse_question(question)
    for elem in parsed:
        if elem.isdigit():
            elem = int(elem)
            
    result : SearchResponse

    return

@app.post("/add")
def add():
    return

#Chiusura della connessione
db_cursor.close()