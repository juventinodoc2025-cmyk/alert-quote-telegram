import os
from telegram import Bot
from flask import Flask

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_test_message():
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text="✅ TEST OK: messaggio inviato da Render"
    )

@app.route("/")
def home():
    return "Service alive"

@app.route("/run")
def run():
    send_test_message()
    return "Telegram test sent"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
