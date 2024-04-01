# Usa l'immagine Docker di Python 3.8
FROM python:3.8

# Imposta la directory di lavoro nel contenitore
WORKDIR /app

# Copia i file del progetto nel contenitore
COPY . .

# Installa le dipendenze
RUN apt-get update && apt-get install -y wget unzip xvfb libxi6 libgconf-2-4
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

RUN pip install -r requirements.txt

# Esegui lo script Python quando il contenitore viene avviato
CMD ["python", "tunefind.py"]
