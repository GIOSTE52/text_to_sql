from src.config.paths import DB_CONFIG, DATA_FILE
from src.utils.parse_data import *

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import mariadb
    
app = FastAPI(title="text_to_sql Server REST")

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

#Imposto il formato del payload da ricevere in input nell'endpoint /add
class AddPayload(BaseModel):
    data_line : str

@app.get("/")
def root()->List[List]:
    try:
        db_conn = mariadb.connect(**DB_CONFIG)
        with open(DATA_FILE, "r") as fd:
            reader = csv.reader(fd, delimiter="\t")
            next(reader)
            for line in reader:
                line = ",".join(line)
                add_to_database(db_conn, line)

        #Stampo l'headers e i valori presenti nella tabella
        table_value = read_tables_values(db_conn, "movies")
        # headers = read_tables_headers(db_conn, "movies")
        # print("TABLE: movies")
        # print("Header:",headers)
        # print("Table_value:",table_value, sep="\n")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Errore, sintassi non valida: {e}")
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Errore durante la connesione al database: {e}")
    finally:
        db_conn.close()
    
    return table_value

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/schema_summary")
def get_schema_summary()->List[TableSchema]:
    try:
        db_conn = mariadb.connect(**DB_CONFIG)
        db_cursor = db_conn.cursor()

        db_cursor.execute("SELECT * FROM movies")
        headers = []
        for attribute in db_cursor.description:
            headers.append(attribute[0])
        
        schema = []
        for col in headers:
            schema.append({
                "table_name": "movies",
                "table_column": str(col)
            })
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Errore durante l'operazione sul database: {e}")
    finally:
        db_cursor.close()
        db_conn.close()
    return schema

@app.get("/search/{question}")
def search(question : str)->List:
    try:
        db_conn = mariadb.connect(**DB_CONFIG)
        db_cursor = db_conn.cursor()

        query = translate_to_query(question)
        if query =="NON RICONOSCIUTA!":
            raise HTTPException(status_code=422, detail="Non è possibile elaborare questa richiesta!" )
        else:
            db_cursor.execute(query)
            result = db_cursor.fetchall()

            if "regista" in query:
                item_type = "director"
            else:
                item_type = "film"
            ret = sql_to_json(result, read_tables_headers(db_conn, "movies"), item_type)
            ret = SearchResponse(
                result=ret
                )
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Errore durante l'operazione sul database: {e}")
    finally:                
        db_cursor.close()
        db_conn.close()
    return ret.result

@app.post("/add")
def add(data_line : AddPayload)-> Dict[str,str]:
    data_line = data_line.data_line
    db_conn = mariadb.connect(**DB_CONFIG)
    try:
        add_to_database(db_conn, data_line)
        ret = {"status" : "ok"}
        # return {"status" : "ok"}
    except ValueError as e:
        ret = {"status" : f"Errore, dati non validi: {e}"}
        raise HTTPException(status_code=422, detail=f"Errore, linea di dati non valida: {e}")
    except mariadb.Error as e:
        ret = {"status" : f"Errore durante un operazione sul database: {e}"}
        raise HTTPException(status_code=500, detail=f"Errore durante l'operazione sul database: {e}")
    finally:
        db_conn.close()
    return ret