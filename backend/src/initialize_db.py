from src.config.paths import DB_CONFIG, DATA_FILE
from src.utils.parse_data import add_to_database

import csv
import mariadb 

API_BASE_URL ="http://backend:8003"


if __name__=="__main__":
    print("Esecuzione dello script initialize_db.py")
    try:
        db_conn = mariadb.connect(**DB_CONFIG)
        with open(DATA_FILE, "r") as fd:
            reader = csv.reader(fd, delimiter="\t")
            next(reader)
            for line in reader:
                line = ",".join(line)
                add_to_database(db_conn, line)
    except ValueError as e:
        print(f"Errore, sintassi non valida: {e}")
    except mariadb.Error as e:
        print(f"Errore durante la connesione al database: {e}")
    finally:
        db_conn.close()
