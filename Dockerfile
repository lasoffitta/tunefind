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

# Scarica e installa ChromeDriver
RUN wget https://filebin.net/rb2gfde5m8yqmbpo/chromedriver -O /usr/local/bin/chromedriver
RUN chmod +x /usr/local/bin/chromedriver

RUN pip install -r requirements.txt

# Espone la porta 80
EXPOSE 80

# Esegui lo script Python quando il contenitore viene avviato
CMD ["python", "tunefind.py"]
