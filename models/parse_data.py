from config.paths import DATA_FILE, QUESTIONS_FILE, DB_CONFIG

from typing import Dict, List, Tuple
import csv
import string
import mariadb

question_to_parsed : Dict[str, List[str]] = {}
parsed_to_query : Dict[str, str] = {}

# Funzione che restituisce i dati letti nel file 
# in una lista di liste, in cui ogni elemento della
# lista( a sua volta una lista) è la riga del file letto
def read_headers_file(file_path:str)->List[str]:
    with open(file_path, "r") as fd:
        reader = csv.reader(fd, delimiter="\t")
        headers : List[str] = []
        headers = next(reader)
        # Print per leggere le righe del file da terminale
        # for line in reader:
        #     print(line)
    return headers
    
# Funzione che parsa una domanda dal file questions.txt e la rende una lista di stringhe senza punteggiatura
def parse_question(question:str)->List[str]:
    parsed : List[str] = question.strip().strip(string.punctuation).split()
    #Print di controllo
    # for s in parsed:
    #     if s.isdigit():
    #         s = int(s)
    #         print(f"{s}, {type(s)}")
    #     else:
    #         print(s)
    return parsed

# Funzione che restituisce in output le varie colonne di una table nel formato richiesto
def read_tables_headers(table_name:str)->List[List[str]]:
    result : List[List[str]] = []
    headers : List[str] = []

    db_conn = mariadb.connect(**DB_CONFIG)
    db_cursor = db_conn.cursor()

    db_cursor.execute(f"SELECT * FROM {table_name}")
    headers = []
    for row in db_cursor.fetchall():
        result.append(row)
    for attribute in db_cursor.description:
        headers.append(attribute[0])

    db_cursor.close()
    return result,headers

# Aggiunge al database i dati forniti in una riga con valori separati da virgola
# e con formato seguente: Titolo, Regista, Età_Autore, Anno, Genere, Piattaforma_1, Piattaforma_2
def add_to_database(data_line:str)->None:
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
    db_cursor.execute("INSERT INTO film VALUES (?,?,?,?,?,?)", insert_data)
    db_conn.commit()

    db_cursor.close()
    return

if __name__=="__main__":
    # headers_file = read_headers_file(DATA_FILE)
    with open(QUESTIONS_FILE, "r") as fd:
        for line in fd:
            print(line)
            parsed = parse_question(line)
            question_to_parsed[line] = parsed
    # Stampo il dizionario che traduce in una lista di stringhe la stringa letta dal file questions.txt
    # print(question_to_parsed)

    table_value, headers = read_tables_headers("film")
    print("TABLE: film")
    print("Header:",headers)
    print("Table_value:",table_value)

    table_value, headers = read_tables_headers("registi")
    print("TABLE: registi")
    print("Header:",headers)
    print("Table_value:",table_value)

    # Dati usati come esempio 
    # input = "Inception, Christopher Nolan, 54, 2010, Fantascienza, Amazon Prime Video, NOW"
    # add_to_database(input)
    with open(DATA_FILE, "r") as fd:
        # Da impostare il delimiter="," alla fine del progetto
        # reader = csv.reader(fd, delimiter=",")
        reader = csv.reader(fd, delimiter="\t")
        next(reader)
        for line in reader:
            print(line)
            add_to_database(line)
