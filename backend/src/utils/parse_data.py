from config.paths import DATA_FILE, QUESTIONS_FILE, DB_CONFIG

from typing import Dict, List, Tuple
import csv
import string
import mariadb

question_to_parsed : Dict[str, List[str]] = {}
parsed_to_query : Dict[str, str] = {}
question_to_query : Dict[str, str] = {}

# Funzione che restituisce l'headers del file .tsv come lista di stringhe
def read_headers_file(file_path:str)->List[str]:
    with open(file_path, "r") as fd:
        reader = csv.reader(fd, delimiter="\t")
        headers : List[str] = []
        headers = next(reader)
        # Print per leggere le righe del file da terminale
        # for line in reader:
        #     print(line)
    return headers
    
# Funzione che parsa una domanda dal file questions.txt e la traduce in una lista di stringhe senza punteggiatura
# e popola il dizionario question_to_parsed con esse
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

# Funzione che popola il dizionario in cui ogni domanda ha un corrispettivo come query SQL
def translate_to_query(question:str)->str:
    question = question.strip()

    if question.startswith("Elenca i film del "):
        anno = question.replace("Elenca i film del ", "")
        return f"SELECT * FROM movies WHERE anno = {anno}"
    elif question.startswith("Quali sono i registi presenti su Netflix?"):
        return "SELECT regista FROM movies WHERE piattaforma_1 = 'Netflix' OR piattaforma_2='Netflix'"
    elif question.startswith("Elenca tutti i film di fantascienza."):
        return "SELECT * FROM movies WHERE genere='Fantascienza'"
    elif question.startswith("Quali film sono stati fatti da un regista di almeno ") and question.endswith(" anni?"):
        inizio = "Quali film sono stati fatti da un regista di almeno "
        fine = " anni?"
        eta = question[len(inizio):-len(fine)]
        if eta.isdigit():
            eta = int(eta)
            return f"SELECT * FROM movies WHERE eta_autore >= {eta}"  
    elif question.startswith("Quali registi hanno fatto più di un film?"):
        return "SELECT regista FROM movies WHERE IN (SELECT regista FROM movies GROUP BY regista HAVING count(*) > 1)"
    else:
        return "QUESTION NON RICONOSCIUTA!"


# Funzione che restituisce in output le varie righe e i nomi delle colonne di una table
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
    db_conn = mariadb.connect(**DB_CONFIG)
    db_cursor = db_conn.cursor()
    
    #La riga sottostante serve solo se il parametro è letto da un testo txt oppure non è stato parsato prima,
    #in questo caso lo leggo da un file csv quindi viene parsato dal reader, da cambiare alla fine del progetto 
    parsed = data_line.strip().split(",")
    parsed = data_line

    film_title = parsed[0].strip()
    director_name = parsed[1].strip()
    director_age = parsed[2].strip()
    film_year = parsed[3].strip()
    film_genr = parsed[4].strip()
    platform_1 = parsed[5].strip()
    platform_2 = parsed[6].strip()

    # Vedo se il regista o il titolo esiste di già ed eseguo l'update
    db_cursor.execute(f"SELECT * FROM movies WHERE regista='{director_name}'")
    regista = db_cursor.fetchone()
    db_cursor.execute(f"SELECT * FROM movies WHERE titolo='{film_title}'")
    titolo = db_cursor.fetchone()
    #fetchone() ritorna None se non ci sono dati corrispondenti, altrimenti ritorna la lista di tuple corrispondente al risultato della query effettuata
    
    #
    if regista is not None:
        try:
            update_data = (film_title, director_age, film_year, film_genr, platform_1, platform_2)
            db_cursor.execute("UPDATE movies SET titolo = ?, eta_autore = ?, anno = ?, genere = ?, piattaforma_1 = ?, piattaforma_2 = ?", update_data)
            db_conn.commit()
        except mariadb.Error as e:
            print(f"Errore durante l'operazione UPDATE: {e}")
                        
    if titolo is not None:
        try:
            update_data = (director_name, director_age, film_year, film_genr, platform_1, platform_2)
            db_cursor.execute("UPDATE movies SET regista = ?, eta_autore = ?, anno = ?, genere = ?, piattaforma_1 = ?, piattaforma_2 = ?", update_data)
            db_conn.commit()
        except mariadb.Error as e:
            print(f"Errore durante l'operazione UPDATE: {e}")

    insert_data = (film_title, director_name, director_age, film_year, film_genr, platform_1, platform_2)
    try:
        db_cursor.execute("INSERT INTO movies(titolo, regista, eta_autore, anno, genere, piattaforma_1, piattaforma_2) VALUES (?,?,?,?,?,?,?)", insert_data)
        db_conn.commit()
    except mariadb.Error as e:
        print(f"Errore nell'esecuzione di una query INSERT: {e}")
        exit(1)

        
    db_cursor.close()
    return



if __name__=="__main__":
    # headers_file = read_headers_file(DATA_FILE)
    
    #Popolo il dizionario delle domande parsate
    with open(QUESTIONS_FILE, "r") as fd:
        for line in fd:
            parsed = parse_question(line)
            question_to_parsed[line] = parsed

    # Stampo il dizionario che traduce in una lista di stringhe la stringa letta dal file questions.txt
    print(question_to_parsed)

    #Stampo gli headers e i valori delle tabelle del database
    table_value, headers = read_tables_headers("movies")
    print("TABLE: movies")
    print("Header:",headers)
    print("Table_value:",table_value)

"""
    #Aggiungo al database i dati inseriti da un file formato csv
    with open(DATA_FILE, "r") as fd:
        # Da impostare il delimiter="," alla fine del progetto
        # reader = csv.reader(fd, delimiter=",")
        reader = csv.reader(fd, delimiter="\t")

        next(reader)
        for line in reader:
            print(line)
            add_to_database(line)
"""
    # table_value, headers = read_tables_headers("registi")
    # print("TABLE: registi")
    # print("Header:",headers)
    # print("Table_value:",table_value)
