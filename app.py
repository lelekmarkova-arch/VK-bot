import json
import requests
import random
from flask import Flask, request

app = Flask(__name__)

TOKEN = "vk1.a.Yl53xSewO4g1Zsy1uP9eQkbwgyp8lELb4noR0GV-iz9f3Pu3Z7nZDqAwXiTqfiQkKmR38iULc3eu5IaAr4Wad5a5uRofrt2Q9Gmd4UcitbfGgObbgysfRYCPcS7VqiQZNS7Ul0y_e0DDjZV-9bYhUJFI2MJMbeBimIlw3nxSpXRlSm7pGgaVzOuI52EUgojPR4ngJEyI7X12M5IfrFidUQ"
CONFIRMATION_TOKEN = "d92bddc6"

processed_events = set()

# 📄 ДОКУМЕНТЫ VK
DOCS = {
    "штатка": "doc270527743_702121234",
    "согласие": "doc270527743_702121233",
    "купля": "doc270527743_702121232",
    "комиссия": "doc270527743_702121241"
}

# 🎛 КНОПКИ
def get_keyboard():
    keyboard = {
        "one_time": False,
        "buttons": [
            [{"action": {"type": "text", "label": "📊 Штатное расписание"}, "color": "primary"}],
            [{"action": {"type": "text", "label": "🛡️ Согласие ПД"}, "color": "primary"}],
            [{"action": {"type": "text", "label": "🏠 Купля-продажа"}, "color": "secondary"}],
            [{"action": {"type": "text", "label": "📄 Договор комиссии"}, "color": "secondary"}]
        ]
    }
    return json.dumps(keyboard, ensure_ascii=False)


# 📤 ОТПРАВКА СООБЩЕНИЯ (СТАБИЛЬНАЯ ВЕРСИЯ)
def send_message(user_id, message=None, attachment=None):
    try:
        params = {
            "peer_id": user_id,
            "message": message or "",
            "random_id": random.randint(1, 10**9),
            "access_token": TOKEN,
            "v": "5.131"
        }

        if attachment:
            params["attachment"] = attachment

        requests.post(
            "https://api.vk.com/method/messages.send",
            params=params
        )

    except Exception as e:
        print("VK SEND ERROR:", e)


# 🚀 ping (Render)
@app.route("/ping", methods=["GET"])
def ping():
    return "OK", 200


# 🤖 CALLBACK VK
@app.route("/", methods=["POST"])
def vk_callback():
    data = request.get_json(silent=True) or {}

    if data.get("type") == "confirmation":
        return CONFIRMATION_TOKEN

    if data.get("type") != "message_new":
        return "ok"

    event_id = data.get("event_id")
    if event_id in processed_events:
        return "ok"
    processed_events.add(event_id)

    msg = data.get("object", {}).get("message", {})
    user_id = msg.get("from_id")
    text = (msg.get("text") or "").lower()

    if not user_id:
        return "ok"

    # 👋 старт
    if text in ["начать", "start", "привет"]:
        send_message(user_id, "👋 Привет! Выберите документ ниже 👇")

    # 📊 штатка
    elif "штат" in text:
        send_message(user_id, "📊 Штатное расписание", DOCS["штатка"])

    # 🛡 согласие
    elif "соглас" in text:
        send_message(user_id, "🛡️ Согласие на обработку ПД", DOCS["согласие"])

    # 🏠 купля-продажа
    elif "купля" in text or "продаж" in text:
        send_message(user_id, "🏠 Договор купли-продажи", DOCS["купля"])

    # 📄 комиссия
    elif "комис" in text:
        send_message(user_id, "📄 Договор комиссии", DOCS["комиссия"])

    else:
        send_message(user_id, "Выберите кнопку ниже 👇")

    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
