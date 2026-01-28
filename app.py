from flask import Flask
import os
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return "Telegram not configured"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, json=payload)

@app.route("/")
def home():
    return "Service alive"

@app.route("/run")
def run_check():
    send_telegram("✅ Cron attivo: servizio funzionante")
    return "OK"

if __name__ == "__main__":
    app.run()
