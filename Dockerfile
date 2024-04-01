# Usa l'immagine Docker di Python 3.8
FROM python:3.8

# Imposta la directory di lavoro nel contenitore
WORKDIR /app

# Copia i file del progetto nel contenitore
COPY . .

# Installa le dipendenze
RUN pip install -r requirements.txt

# Esegui lo script Python quando il contenitore viene avviato
CMD ["python", "tunefind.py"]
