from src.config.paths import DATA_FILE, QUESTIONS_FILE, DB_CONFIG

from typing import Dict, List, Tuple
from pydantic import BaseModel
import csv
import string
import mariadb

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
    question = question.strip(string.punctuation)

    if question.startswith("Elenca i film del "):
        anno = question.replace("Elenca i film del ", "")
        if anno.isdigit():
            anno = int(anno)
            return f"SELECT titolo, regista, eta_autore, anno, genere, piattaforma_1, piattaforma_2 FROM movies WHERE anno = {anno}"
        
    elif question.startswith("Quali sono i registi presenti su Netflix"):
        return "SELECT regista FROM movies WHERE piattaforma_1 = 'Netflix' OR piattaforma_2='Netflix'"
    
    elif question.startswith("Elenca tutti i film di fantascienza"):
        return "SELECT titolo, regista, eta_autore, anno, genere, piattaforma_1, piattaforma_2 FROM movies WHERE genere='Fantascienza'"
    
    elif question.startswith("Quali film sono stati fatti da un regista di almeno ") and question.endswith(" anni"):
        inizio = "Quali film sono stati fatti da un regista di almeno "
        fine = " anni"
        eta = question[len(inizio):-len(fine)]
        if eta.isdigit():
            eta = int(eta)
            return f"SELECT titolo, regista, eta_autore, anno, genere, piattaforma_1, piattaforma_2 FROM movies WHERE eta_autore >= {eta}"  
        
    elif question.startswith("Quali registi hanno fatto più di un film"):
        return "SELECT regista FROM movies WHERE regista IN (SELECT regista FROM movies GROUP BY regista HAVING count(*) > 1)"
    
    else:
        return "NON RICONOSCIUTA!"

# Fuznione che restituisce i valori delle tuple della tabella identificata da table_name
def read_tables_values(db_conn:mariadb.Connection, table_name:str)->List[List[str]]:
    result : List[List[str]] = []
    db_cursor = db_conn.cursor()

    db_cursor.execute(f"SELECT titolo, regista, eta_autore, anno, genere, piattaforma_1, piattaforma_2 FROM {table_name}")
    for row in db_cursor.fetchall():
        result.append(row)

    db_cursor.close()
    return result

# Funzione che restituisce in output i nomi delle colonne di una table identificata da table_name
def read_tables_headers(db_conn:mariadb.Connection, table_name:str)->List[str]:
    headers : List[str] = []
    db_cursor = db_conn.cursor()

    db_cursor.execute(f"SELECT * FROM {table_name}")
    headers = []
    for param in db_cursor.description:
        headers.append(param[0])

    db_cursor.close()
    return headers

# Aggiunge al database i dati forniti in una riga con valori separati da virgola
# e con formato seguente: Titolo, Regista, Età_Autore, Anno, Genere, Piattaforma_1, Piattaforma_2
# La connessione al database viene passata come parametro
def add_to_database(db_conn : mariadb.Connection, data_line:str)->None:
    
    db_cursor : mariadb.Cursor= db_conn.cursor()
    try:
        if data_line.count(",") != 6:
            raise ValueError("La riga fornita non contiene esattamente 7 campi separati da virgola")

        parsed = data_line.strip().split(",")

        if len(parsed) != 7:
            raise ValueError("La riga fornita non contiene esattamente 7 campi")

        cont = 0
        #Gestisco le occorrenze di apostrofi non desiderati nelle query da effettuare
        for elem in parsed:
            if "'" in elem:
                parsed[cont] = elem.replace("'"," ")
                cont += 1

        film_title = parsed[0].strip()
        director_name = parsed[1].strip()
        director_age = parsed[2].strip()
        film_year = parsed[3].strip()
        film_genr = parsed[4].strip()
        platform_1 = parsed[5].strip()
        platform_2 = parsed[6].strip()

        #Gestisco i casi in cui il regista o il titolo vengono modificati all'inserimento di un film, allora aggiorno tutte le occorrenze
        #ed il caso in cui viene aggiunto un film già esistente con diverso regista, per cui devo modificare la vecchia occorrenza eliminando il titolo e lasciando
        #il vechio regista, ma al contempo creare una nuova tupla con il nuovo regista e il titolo del film
        db_cursor.execute(f"SELECT titolo, regista, eta_autore, anno, genere, piattaforma_1, piattaforma_2 FROM movies WHERE titolo='{film_title}'")
        query_result = db_cursor.fetchone()

        #DA TENERE A MENTE:
        #fetchall() ritorna una lista vuota se non ci sono dati corrispondenti, altrimenti ritorna la lista di tuple corrispondente al risultato della query effettuata
        #fetchone() ritorna None se non ci sono dati corrispondenti, altrimenti ritorna la singola tupla corrispondente al risultato della query effettuata

        if query_result is not None:
            #Prima controllo se esistono film con lo stesso titolo e quindi aggiorno i vari campi con i nuovi valori inseriti
            update_data = (director_name, director_age, film_year, film_genr, platform_1, platform_2)
            db_cursor.execute(f"UPDATE movies SET regista = ?, eta_autore = ?, anno = ?, genere = ?, piattaforma_1 = ?, piattaforma_2 = ? WHERE titolo = '{film_title}'", update_data)
            db_conn.commit()
            #Controllo se il regista sta cambiando rispetto al film omonimo trovato 
            if query_result[1] != director_name:
                #Il regista cambia, quindi controllo se il vecchio regista ha solo un film
                db_cursor.execute(f"SELECT count(*) FROM movies WHERE regista = '{query_result[1]}'")
                num_film = db_cursor.fetchone()[0]
                if num_film > 1:
                    insert_data = (None, query_result[1], query_result[2], query_result[3], query_result[4], query_result[5], query_result[6])
                    db_cursor.execute("INSERT INTO movies (titolo, regista, eta_autore, anno, genere, piattaforma_1, piattaforma_2) VALUES (?,?,?,?,?,?,?)", insert_data)
                    db_conn.commit()




        else:
            insert_data = (film_title, director_name, director_age, film_year, film_genr, platform_1, platform_2)
            db_cursor.execute("INSERT INTO movies(titolo, regista, eta_autore, anno, genere, piattaforma_1, piattaforma_2) VALUES (?,?,?,?,?,?,?)", insert_data)
            db_conn.commit()

    except ValueError as e:
        print(f"Errore, dati inseriti non validi: {e}")
        raise
    except mariadb.Error as e:
        print(f"Errore durante un'operazione sul database: {e}")
        raise
    finally:
        db_cursor.close()
    return

def sql_to_json(result : List[Tuple], columns : List, item_type : str)->SearchResponse:
    ret = []
    #Itero sulle tuple risultanti dalla query SQL e creo un elemento film per ognuna
    for row in result:
        elem = {
            "item_type" : item_type,
            "properties" : []
        }
        cont = 0
        #Itero sui nomi degli attributi in modo da assegnare al corretto attributo il suo valore
        for col,value in zip(columns[1:], row):
            if str(col) == "titolo" or str(col) == "regista":
                item = {
                    "property_name" : "name",
                    "property_value" :  str(value)
                }        
            else:
                item = {
                    "property_name" : str(col),
                    "property_value" :  str(value)
                }        

            elem["properties"].append(item)
        ret.append(elem)

    return ret

# if __name__=="__main__":

    # headers_file = read_headers_file(DATA_FILE)
    
    #Popolo il dizionario con le domande e le rispettive query (non ce n'è bisogno)
    # with open(QUESTIONS_FILE, "r") as fd:
    #     for line in fd:
    #         query = translate_to_query(line)
    #         question_to_query[line] = query

    # # Stampo il dizionario che traduce in una lista di stringhe la stringa letta dal file questions.txt
    # print(question_to_query)

    # #Stampo gli headers e i valori delle tabelle del database
    # db_conn = mariadb.connect(**DB_CONFIG)
    # table_value = read_tables_values(db_conn, "movies")
    # headers = read_tables_headers(db_conn, "movies")
    # print("TABLE: movies")
    # print("Header:",headers)
    # print("Table_value:",table_value)
    # db_conn.close()


    # #Aggiungo al database i dati inseriti da un file formato csv
    # with open(DATA_FILE, "r") as fd:
    #     # Da impostare il delimiter="," alla fine del progetto
    #     # reader = csv.reader(fd, delimiter=",")
    #     reader = csv.reader(fd, delimiter="\t")

    #     next(reader)
    #     for line in reader:
    #         print(line)
    #         add_to_database(line)