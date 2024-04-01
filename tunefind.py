from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from telegram import Bot
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
import os
import time

# Ottieni il token del bot di Telegram dall'ambiente
TELEGRAM_TOKEN_BOT = os.getenv('TELEGRAM_TOKEN_BOT')

# Crea un'istanza del bot di Telegram
bot = Bot(token=TELEGRAM_TOKEN_BOT)

# Crea un'istanza del driver del browser
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def handle_message(update, context):
    # Ottieni l'URL dal messaggio dell'utente
    url = update.message.text

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

# Crea un'istanza dell'Updater
updater = Updater(token=TELEGRAM_TOKEN_BOT, use_context=True)

# Ottieni il dispatcher da utilizzare per registrare gli handler
dp = updater.dispatcher

# Aggiungi un gestore di messaggi al dispatcher
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Avvia il bot
updater.start_polling()

# Blocca fino a quando non viene premuto Ctrl-C o il processo non riceve SIGINT,
# SIGTERM o SIGABRT. Questo dovrebbe essere usato maggiormente per il blocco del thread.
updater.idle()
