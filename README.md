# Text to SQL

**Esonero LabIngInf** - Un progetto per la conversione di testo in query SQL.

## 📋 Descrizione

Questo progetto consente di convertire testo naturale in query SQL, facilitando l'interazione con database attraverso il linguaggio naturale.

## 🛠️ Tecnologie Utilizzate

- **Python** (71.5%) - Logica principale e backend
- **HTML** (25.8%) - Interfaccia web
- **Dockerfile** (2.7%) - Containerizzazione

## 🚀 Avvio

### Requisiti
- Python 3.x
- Docker (opzionale, per containerizzazione)

### Installazione

1. Clona il repository:
```bash
git clone https://github.com/GIOSTE52/text_to_sql.git
cd text_to_sql
```

2. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

3. Avvia l'applicazione:
```bash
python app.py
```

### Con Docker

```bash
docker build -t text_to_sql .
docker run -p 5000:8000 text_to_sql
```

## 📝 Utilizzo

L'applicazione fornisce un'interfaccia web dove puoi inserire testo naturale e ottenere la corrispondente query SQL.

## 📂 Struttura del Progetto

```
text_to_sql/
├── app.py                 # Applicazione principale
├── requirements.txt       # Dipendenze Python
├── Dockerfile            # Configurazione Docker
├── README.md             # Questo file
└── templates/            # File HTML
```

## ✨ Funzionalità

- Conversione da linguaggio naturale a SQL
- Interfaccia web intuitiva
- Supporto per query SQL complesse

## 📧 Contatti

Per domande o suggerimenti, apri un'issue nel repository.

---

**Autore**: GIOSTE52
