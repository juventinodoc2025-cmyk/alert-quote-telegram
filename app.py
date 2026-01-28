import os
import requests
from flask import Flask

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

TARGET_ODDS = 1.03

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    requests.post(url, json=payload)

@app.route("/")
def home():
    return "OK", 200

@app.route("/check")
def check_odds():
    current_odds = 1.05  # simulazione

    if current_odds >= TARGET_ODDS:
        send_telegram_message(
            f"🚨 Over 0.5 arrivato a quota {current_odds}"
        )
        return "Alert sent", 200

    return "No alert", 200
