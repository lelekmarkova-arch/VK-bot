import json
import requests
import random
from flask import Flask, request

app = Flask(__name__)

TOKEN = "vk1.a.Yl53xSewO4g1Zsy1u9ePkbwgyp8lELb4noR0GV-iz9f3Pu3Z7nZDqAwXiTqfiQkKmR38iULc3eu5IaAr4Wad5a5uRofrt2Q9Gmd4UcitbfGgObbgysfRYCPcS7VqiQZNS7Ul0y_e0DDjZV-9bYhUJFI2MJMbeBimIlw3nxSpXRlSm7pGgaVzOuI52EUgojPR4ngJEyI7X12M5IfrFidUQ"
CONFIRMATION_TOKEN = "d92bddc6"


def get_keyboard():
    keyboard = {
        "one_time": False,
        "buttons": [
            [
                {"action": {"type": "text", "label": "📄 Шаблоны документов"}, "color": "primary"},
                {"action": {"type": "text", "label": "❓ Вопросы"}, "color": "secondary"}
            ]
        ]
    }
    return json.dumps(keyboard, ensure_ascii=False)


def send_message(user_id, message):
    requests.post("https://api.vk.com/method/messages.send", data={
        "user_id": user_id,
        "message": message,
        "random_id": random.randint(1, 10**9),
        "keyboard": get_keyboard(),
        "access_token": TOKEN,
        "v": "5.131"
    })


@app.route("/ping", methods=["GET"])
def ping():
    return "OK", 200


@app.route("/", methods=["POST"])
def vk_callback():
    data = request.get_json(silent=True) or {}

    if data.get("type") == "confirmation":
        return CONFIRMATION_TOKEN

    if data.get("type") == "message_new":

        msg = data.get("object", {}).get("message", {})
        user_id = msg.get("from_id")
        text = (msg.get("text") or "").lower()

        if text in ["начать", "start", ""]:
            reply = (
                "👋 Привет! Я бот «Фемистокл»\n\n"
                "📚 Я помогаю малому бизнесу:\n"
                "• шаблоны документов\n"
            )

        elif "шаблон" in text:
            reply = (
                "📄 Шаблоны документов:\n"
                "• договор аренды\n"
                "• договор купли-продажи\n"
                "• договор подряда\n"
                "• претензия\n"
                "• жалоба"
            )

        # 🔥 ИСПРАВЛЕНО ТОЛЬКО ЭТО
        elif text == "❓ вопросы":
            reply = (
                "❓ Вопросы:\n\n"
                "Сейчас бот работает только с шаблонами документов:\n"
                "📄 договор аренды\n"
                "📄 договор купли-продажи\n"
                "📄 договор подряда\n"
                "📄 претензия\n"
                "📄 жалоба"
            )

        else:
            reply = "Выберите кнопку ниже 👇"

        send_message(user_id, reply)

    return "ok"
