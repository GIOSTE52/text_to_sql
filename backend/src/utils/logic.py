from config.paths import DATA_FILE, QUESTIONS_FILE, DB_CONFIG

from typing import Dict, List, Tuple
import csv
import string
import mariadb

#Vecchia implementazione nel caso di due tabelle : movies e registi
def add_to_database(data_line:str)->None:
    # Non serve perchè il csv.reader già restituisce liste di stringhe
    # parsed = data_line.strip().split(",")
    parsed = data_line
    db_conn = mariadb.connect(**DB_CONFIG)
    db_cursor = db_conn.cursor()

    film_title = parsed[0].strip()
    director_name = parsed[1].strip()
    director_age = parsed[2].strip()
    film_year = parsed[3].strip()
    film_genr = parsed[4].strip()
    platform_1 = parsed[5].strip()
    platform_2 = parsed[6].strip()
    # Vedo se il regista esiste di già e ne recupero l'id
    db_cursor.execute(f"SELECT id_regista FROM registi WHERE nome_completo='{director_name}'")
    id_regista = db_cursor.fetchone()
    if id_regista is None:
        insert_data = (director_name, director_age)
        db_cursor.execute("INSERT INTO registi(nome_completo, eta) VALUES (?,?)", insert_data)
        db_conn.commit()

        db_cursor.execute(f"SELECT id_regista FROM registi WHERE nome_completo='{director_name}'")
        id_regista = db_cursor.fetchone()

    if id_regista:
        id_regista = id_regista[0]
    else:
        id_regista = None

    insert_data = (film_title, id_regista, film_year, film_genr, platform_1, platform_2)
    db_cursor.execute("INSERT INTO movies VALUES (?,?,?,?,?,?)", insert_data)
    db_conn.commit()

    db_cursor.close()
    return

if __name__=="__main__":
    #Aggiungo al database i dati inseriti da file formato csv
    with open(DATA_FILE, "r") as fd:
        # Da impostare il delimiter="," alla fine del progetto
        # reader = csv.reader(fd, delimiter=",")
        reader = csv.reader(fd, delimiter="\t")

        next(reader)
        for line in reader:
            print(line)
            add_to_database(line)
