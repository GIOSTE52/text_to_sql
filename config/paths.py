from pathlib import Path

# Root directory del progetto (radice)
ROOT_DIR = Path(__file__).resolve().parent.parent

# Percorsi backend e frontend
BACKEND_SRC_DIR = ROOT_DIR/"backend"/"src"
FRONTEND_SRC_DIR = ROOT_DIR/"frontend"/"src"
TEMPLATES_DIR = ROOT_DIR/"frontend"/"templates"

# Percorso ai moduli
MODELS_DIR = ROOT_DIR/"models"

# Percorsi ai dati riguardo il databasepa
DATA_DIR = ROOT_DIR/"mariadb_data"
INIT_SQL_DIR = ROOT_DIR/"mariadb_init"

DATA_FILE = DATA_DIR/"data.tsv"
QUESTIONS_FILE = DATA_DIR/"questions.txt"
INIT_SQL = INIT_SQL_DIR/"init.sql"
DELETE_SQL = INIT_SQL_DIR/"delete.sql"

# Percorso ai test
TESTS_DIR = ROOT_DIR/"tests"

# Parametri di configurazione della connessione al DB
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3307,
    "user": "root",
    "password": "rootpassword",
    "database": "text_to_sql_DB"
}

#Se eseguito singolarmente stampa i path per verificare che funzioni (FUNZIONA)
if __name__ == "__main__":
    print(f"Backend dir: {BACKEND_SRC_DIR}")
    print(f"Data file: {DATA_FILE}")
