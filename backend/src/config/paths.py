from pathlib import Path

# Root directory del progetto (radice)
ROOT_DIR = Path(__file__).resolve().parent.parent

# Percorsi backend e frontend
BACKEND_SRC_DIR = ROOT_DIR/"backend"/"src"
FRONTEND_SRC_DIR = ROOT_DIR/"frontend"/"src"
TEMPLATES_DIR = ROOT_DIR/"frontend"/"templates"

# Percorsi ai dati riguardo il database

# DATA_DIR = ROOT_DIR/"backend"/"data"
DATA_DIR = Path("/backend/data")

DATA_FILE = DATA_DIR/"data.tsv"
QUESTIONS_FILE = DATA_DIR/"questions.txt"


# Parametri di configurazione della connessione al DB
# Qua sotto ho i parametri di configurazione della connessione al DB per i test manuali
# DB_CONFIG = {
#     "host": "127.0.0.1",
#     "port": 3307,
#     "user": "root",
#     "password": "rootpassword",
#     "database": "text_to_sql_DB"
# }
DB_CONFIG = {
    "host" : "database",
    "port" : 3306,
    "user" : "stefano",
    "password" : "pwd",
    "database" : "text_to_sql_DB"
}

#Stampa i path per verificare che funzioni (FUNZIONA)
if __name__ == "__main__":
    print(f"Backend dir: {BACKEND_SRC_DIR}")
    print(f"Data file: {DATA_FILE}")
