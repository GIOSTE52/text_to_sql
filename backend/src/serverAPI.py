from config.paths import DB_CONFIG

from fastapi import FastAPI, HTTPException, requests
from pydantic import BaseModel
from typing import List
import mariadb
    
app = FastAPI(title="text_to_sql")

#Imposto il formato delle tabelle da restituire in output alla richiesta GET schema_summary
class TableSchema(BaseModel):
    table_name : str
    table_column : str


#Gestisco possibili errori durante la connessione al database
try:
    # db_conn = mariadb.connect(
    #     host="127.0.0.1",
    #     port=3307,
    #     user="stefano",
    #     password="pwd",
    #     database="text_to_sql_DB"
    # )
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


#Chiusura della connessione
db_cursor.close()