import os
import requests
from flask import Flask
from datetime import datetime

app = Flask(__name__)

# === ENV ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
ODDS_API_KEY = os.getenv("ODDS_API_KEY")
MATCH_KEYWORD = os.getenv("MATCH_KEYWORD", "").lower()

BOOKMAKER = "bet365"
TARGET_ODDS = 1.03

ALERT_FILE = "alert_day.txt"
EVENT_FILE = "event_id.txt"

def today():
    return datetime.utcnow().strftime("%Y-%m-%d")

def send_telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={"chat_id": TELEGRAM_CHAT_ID, "text": msg},
        timeout=10
    )

def alert_already_sent():
    if not os.path.exists(ALERT_FILE):
        return False
    with open(ALERT_FILE) as f:
        return f.read().strip() == today()

def mark_alert_sent():
    with open(ALERT_FILE, "w") as f:
        f.write(today())

def get_saved_event():
    if not os.path.exists(EVENT_FILE):
        return None
    with open(EVENT_FILE) as f:
        return f.read().strip()

def save_event(event_id):
    with open(EVENT_FILE, "w") as f:
        f.write(event_id)

def find_event_by_keyword():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "eu",
        "markets": "over_under",
        "bookmakers": BOOKMAKER
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    for event in data:
        name = f"{event.get('home_team','')} {event.get('away_team','')}".lower()
        if MATCH_KEYWORD and MATCH_KEYWORD in name:
            save_event(event["id"])
            return event["id"]

    return None

@app.route("/check")
def check():
    if alert_already_sent():
        return "Alert già inviato"

    event_id = get_saved_event()
    if not event_id:
        event_id = find_event_by_keyword()
        if not event_id:
            return "Partita non trovata"

    url = "https://api.the-odds-api.com/v4/sports/soccer/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "eu",
        "markets": "over_under",
        "bookmakers": BOOKMAKER,
        "eventIds": event_id,
        "oddsFormat": "decimal"
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    if not data:
        return "Evento non disponibile"

    for bookmaker in data[0]["bookmakers"]:
        for market in bookmaker["markets"]:
            for outcome in market["outcomes"]:
                if outcome["name"] == "Over" and outcome["point"] == 0.5:
                    quota = outcome["price"]
                    if quota >= TARGET_ODDS:
                        send_telegram(
                            f"🚨 {MATCH_KEYWORD.upper()} – Over 0.5 a quota {quota}"
                        )
                        mark_alert_sent()
                        return "Alert inviato"

    return "Quota non raggiunta"

@app.route("/")
def home():
    return "Bot attivo"
