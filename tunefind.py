from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters
from telegram.ext import CommandHandler
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import requests
import time

app = Flask(__name__)

# Ottieni il token del bot di Telegram dall'ambiente
TELEGRAM_TOKEN_BOT = os.getenv('TELEGRAM_TOKEN_BOT')

# Crea un'istanza del bot di Telegram
bot = Bot(token=TELEGRAM_TOKEN_BOT)

# Crea un'istanza del driver del browser
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)
driver.set_page_load_timeout(30)

@app.route('/')
def home():
    return "Benvenuto al bot di Telegram per Tunefind!"

def set_webhook():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN_BOT}/setWebhook"
    params = {'url': 'https://tunefind.onrender.com/' + TELEGRAM_TOKEN_BOT}
    r = requests.post(url, params=params)
    print(r.json())

def handle_message(update, context):
    # Ottieni l'URL dal messaggio dell'utente
    url = update.message.text

    # Verifica che l'URL sia un URL valido da tunefind.com
    if 'tunefind.com' not in url:
        bot.send_message(chat_id=update.message.chat_id, text="Per favore, inserisci un URL valido da tunefind.com.")
        return

    # Vai alla pagina web
    driver.get(url)

    # Aspetta che il pulsante "Show all tracks" sia presente e fai clic su di esso
    try:
        show_all_tracks_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//p[text()="Show all tracks"]')))
        show_all_tracks_button.click()
        # Aspetta un po' per permettere al sito di caricare i nuovi brani
        time.sleep(5)
    except:
        bot.send_message(chat_id=update.message.chat_id, text="Non è stato possibile trovare il pulsante 'Show all tracks'.")

    # Trova tutti gli elementi con la classe specifica per i titoli dei brani
    song_elements = driver.find_elements(By.CSS_SELECTOR, '.SongPreviewPlayer___StyledRow2-sc-dfotcz-7.cyJpmy')

    # Per ogni elemento del titolo della canzone, trova l'elemento dell'artista corrispondente e invia l'artista e il titolo della canzone nel formato desiderato
    for song_element in song_elements:
        song_title = song_element.find_element(By.CSS_SELECTOR, '.SongPreviewPlayer___StyledTypography2-sc-dfotcz-9.lkkqNm').text
        artist_name = song_element.find_element(By.CSS_SELECTOR, '.sc-ksBlkl.fQsVMV.sc-iveFHk.lmmTYi').text

        bot.send_message(chat_id=update.message.chat_id, text=artist_name + ' - ' + song_title)

    # Chiudi il driver del browser dopo aver elaborato ogni URL
    driver.quit()

@app.route('/' + TELEGRAM_TOKEN_BOT, methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dp.process_update(update)
    return "OK"

def start(update, context):
    bot.send_message(chat_id=update.message.chat_id, text="Per favore, inserisci un URL valido da tunefind.com.")

if __name__ == "__main__":
    # Crea un'istanza del Dispatcher
    dp = Dispatcher(bot, None, use_context=True)

    # Aggiungi un gestore di comandi al dispatcher
    dp.add_handler(CommandHandler("start", start))

    # Aggiungi un gestore di messaggi al dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Imposta il webhook
    set_webhook()

    # Avvia il bot
    app.run(host="0.0.0.0", port=int(os.getenv('PORT', 5000)))
