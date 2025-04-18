from config.paths import DATA_FILE
from typing import Dict, List
import csv

# Funzione che restituisce i dati letti nel file 
# in una lista di liste, in cui ogni elemento della
# lista( a sua volta una lista) è la riga del file letto

def read_data()->List[List[str]]:
    result : List[List[str]] = []
    table_property : List[List[str]] = []
    with open(DATA_FILE, "r") as data_file:
        reader = csv.reader(data_file, delimiter="\t")
        table_property = next(reader, [])
        for line in reader:
            print(line)
            result.append(line)
    return result
    
