import time
import requests
from telegram import Bot

# === CONFIGURAZIONE (poi la completiamo) ===
TELEGRAM_TOKEN = "INSERISCI_TOKEN_BOT"
TELEGRAM_CHAT_ID = "INSERISCI_CHAT_ID"

# Simulazione quota (per ora)
TARGET_ODDS = 1.03

def send_telegram_message(text):
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)

def main():
    notified = False

    while True:
        current_odds = 1.01  # per ora fissa, poi la colleghiamo alle API

        if current_odds >= TARGET_ODDS and not notified:
            send_telegram_message(
                f"🚨 Over 0.5 arrivato a quota {current_odds}"
            )
            notified = True

        time.sleep(60)  # controlla ogni 60 secondi

if __name__ == "__main__":
    main()
