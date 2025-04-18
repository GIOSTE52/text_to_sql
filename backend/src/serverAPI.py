from fastapi import FastAPI, HTTPException, requests
from pydantic import BaseModel
import mariadb
    
app = FastAPI(title="text_to_sql")

#Gestisco possibili errori durante la connessione al database
try:
    db_conn = mariadb.connect(
        host="127.0.0.1",
        port=3307,
        user="stefano",
        password="pwd",
        database="text_to_sql_DB"
    )
except mariadb.Error as e:
    print(f"Errore nella connessione al database: {e}")
    exit(1)
#Creo il cursore(punto di contatto) per gestire la connessione con il database
db_cursor : mariadb.Cursor = db_conn.cursor()





#Chiusura della connessione
db_cursor.close()